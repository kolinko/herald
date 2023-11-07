import openai

import os

import json
from common import json_fetch, ai, ai3, download_and_cache

from fetch import fetch_article

import tqdm
import paper

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates/"))
#template = environment.get_template("message.txt")


def harvey_request(journalist=None):
    # this is so ugly! no idea how to put prompts into code in a nicer way. 
    # Perhaps should use jinja2 for templating? But then we split parts of logic into two separate files

    harvey_prompt = f'''
I'm writing a parody story about an editorial office of a tabloid paper covering tech news. 

The paper is titled "Hacker Herald", and it's based on Hacker News news.
'''

    if journalist is not None:
        harvey_prompt += f'''
You are:
{journalist['name']}
{journalist['bio']}

Your editor in chief is:'''
    else:
        harvey_prompt += f'''You are the editor in chief:'''

    harvey_prompt+= f'''
{paper.editor_in_chief['name']}
{paper.editor_in_chief['bio']}

Remember that this is a comedy/parody, so make everything factual, but hilariously over-tabloidy. Think comic-book narrative.
    '''

    return harvey_prompt


def make_paper_fifth():
    print('Generating html...')
    with open(paper.issue_fname, 'r') as f:
        paper_out = json.loads(f.read())

    stories = paper_out['stories']
    story_template = env.get_template("story.html")

    for story in stories:
        source_id = story['sources'][0]
        source = json_fetch('item', source_id)


        story_html = story_template.render(story=story, title=story['title'], source=source, child_dir=None, issue_date=paper.issue_date)
        with open(f"{paper.issue}/{story['sources'][0]}.html", 'w') as f:
            f.write(story_html)

    index_template = env.get_template("index.html")
    html = index_template.render(title=paper.title, 
                                 issue_date=paper.issue_date, 
                                 editors_note=paper_out['editors_note'], 
                                 stories=stories, ads=paper_out['ads'],
                                 child_dir="")

    with open(f'{paper.issue}/index.html', 'w') as f:
        f.write(html)

    print('Done!\n\nTo see full paper')
    print(f'open {paper.issue}/index.html')

    index_template = env.get_template("index.html")
    html = index_template.render(title=paper.title, 
                                 issue_date=paper.issue_date, 
                                 editors_note=paper_out['editors_note'], 
                                 stories=stories, ads=paper_out['ads'],
                                 child_dir=f"{paper.issue}/")

    with open(f'index.html', 'w') as f:
        f.write(html)



def make_paper_fourth():
    print('Inventing ads...')

    with open(paper.issue_fname, 'r') as f:
        paper_out = json.loads(f.read())

    stories = ''

    for story in paper_out['stories']:
        stories += '- '+ story['title'] + '\n'

    harvey_prompt = harvey_request(paper.marketer) + '''
Reply in a following json form:
[{'name':'first product name', 'company': 'fake company name', 'description': 'fake two-sentence description', 'price': 'price. doesn't have to be in actual money. can be stuff like "your soul"'}]
    '''

    user_prompt = f'''Harvey walks into your office. He says:
Chuck! We're ready to publish the current issue, but we need some bullshit products to sell to our readers. Invent something that is vaguely related to today's stories. Four things. Go!

    {stories}'''

    res = ai(harvey_prompt, user_prompt)
    try:
        res = json.loads(res)
    except:
        res = ai3('fix json. output only pure json, no comments from your side', res)
        res = json.loads(res)
    paper_out['ads'] = res

    with open(paper.issue_fname, 'w') as f:
        f.write(json.dumps(paper_out, indent=2))


def make_full_story(story):
    short_name = paper.journalist_by_name(story['author'])['short']
    name = story['author']
    bio = paper.journalist_by_name(name)['bio']

    status_dict[short_name] = 'working...'

    source_id = str(story['sources'][0])
    source = json_fetch('item', source_id)
#        print(json.dumps(source))

    story['source_url'] = source['url']
    status_dict[short_name] = "fetching"
    print(f"[{short_name}] fetching {source['url']} \n")
    source_text = fetch_article(source['url']) # can fail if source url doesn't exist. should try other sources then

    if '==error' in source_text:
        print(source_text)

    harvey_prompt = harvey_request({'name': name, 'bio': bio}) + '''
Reply in a following form:
===title
(title here)
===lead
(1-paragraph lead that will go ona  front page)
===text
(4 paragraphs of article text)'''

    user_prompt = f'''
Harvey walks into your office. He says:
"Allright, we have a title, and below is the original. Write a story based on a source! "

Our title: 
{story['title']}

Original:
{source_text}

* If the source is unreadable (e.g. website says you're not allowed to read it as a bot), in article text, complain hilariously about that website not being accessible, and somehow tie it to the main story, which you can then make up based on a title alone. (and say that you're making stuff up).
'''


    result = None
    count=''

    while result is None:
        status_dict[short_name] = "writing"
        reply = ai(harvey_prompt, user_prompt + count)

        required_sections = 'title', 'lead', 'text'
        if any(f'==={s}' not in reply for s in required_sections):
            count += '\nremember about formatting'
            continue

        result = {}
        result['title'] = reply[len('===title '):reply.find('===lead')]
        result['lead'] = reply[reply.find('===lead')+len('===lead '):reply.find('===text')]
        result['text'] = reply[reply.find('===text')+len('===text '):]

    status_dict[short_name] = 'Done'
    return result

import threading
status_dict = {}
import time

def get_full_story(story):
    story['full_story'] = make_full_story(story)
    return story

def make_paper_third(stories_items):
    with open(paper.issue_fname, 'r') as f:
        paper_out = json.loads(f.read())

    print('Writing full stories...\n')

    for story in paper_out['stories']:
        print('writing story')
        get_full_story(story)



    '''
    multi threading
    threads = []
    for story in paper_out['stories']:
        t = threading.Thread(target=get_full_story, args=(story,))
        t.start()
        threads.append(t)

    time.sleep(1)
    cursor_up_code = '\x1b[1A'
    clear_line_code = '\x1b[2K'
    while True:
        print("\t".join([f"{k}: {v}" for k, v in status_dict.items()]))
        time.sleep(1)  # Delay between updates

        if all(value == 'Done' for value in status_dict.values()):  # If all tasks are done
            break

        print(cursor_up_code + cursor_up_code + clear_line_code)#(cursor_up_code + clear_line_code) * len(status_dict), end='\r')
    '''

    print('All done.\n')


#    for t in threads:
#        t.join()

    with open(paper.issue_fname, 'w') as f:
        f.write(json.dumps(paper_out, indent=2))


def make_paper_second():
    print("Writing editors' note...")
    with open(paper.issue_fname, 'r') as f:
        paper_out = json.loads(f.read())

    stories = ''
    for story in paper_out:
        stories += '- ' + story['title'] + '\n'

    harvey_prompt = harvey_request()

    user_prompt = "Your journalists delivered these stories for the day:\n\n"+\
                  stories+'\n\n'+\
                  "Write a brief, two-paragraph editor's note that will fit the front page. The words of wisdom that will encourage your readers to read the rest :)"

    note = ai(harvey_prompt, user_prompt)

    paper_out = {
        'stories': paper_out,
        'editors_note': note,
    }

    with open(paper.issue_fname, 'w') as f:
        f.write(json.dumps(paper_out, indent=2))


def make_paper_first(stories):
    """ prepare a table of contents """
    print('Asking each journalist to choose a subject and write a title for their piece...')
    others = ''

    paper_out = []
    used_up = []

    for journalist in tqdm.tqdm(paper.journalists):
        your_name = journalist['name']
        your_bio = journalist['bio']

        stories_text = ''
        for story_id in stories:
            if story_id not in used_up:
                stories_text += stories[story_id]['ai_text']

        result = choose_stories(your_name, your_bio, others, stories_text)
  
        # TODO: make Harvey choose the best story
        picked = result[0]
        picked['sources'] = [str(src) for src in picked['sources']]

        print(f'picked: {picked["title"]}')

        used_up += picked['sources']

        if others == '':
            others = 'Others already took these stories, so pick something else than them:\n'
        
        others += picked['title'] + '\n'
        picked['author'] = your_name
        paper_out.append(picked)

        print(json.dumps(result, indent=2))

        print('paper so far:')
        print(json.dumps(paper_out, indent=2))

    with open(paper.issue_fname, 'w') as f:
        f.write(json.dumps(paper_out, indent=2))


def choose_stories(your_name, your_bio, others, stories):
    print(f'Asking {your_name}...')

    harvey_prompt = harvey_request({'name':your_name, 'bio':your_bio}) + '''
If you get asked to write a story, choose one theme, don't merge various themes.

Reformat the reply to be in json:
{'stories':[{"why":(five words why this story fits your speciality), "title":..., "sources":[source_ids],"title":...},{"why":...}]}

Three titles max, three sources max per title. 
'''

    user_prompt = "Harvey, leaning on your desk with an intense expression, demands, " +\
                  "We need a front-page story from you for the day. " +\
                  "Pick something from this list and whip up a headline that'll make our readers' jaws drop!\n\n" +\
                     others + "\n\n" +\
                     stories

    while True:
        out_txt = ai(harvey_prompt, user_prompt, json=True)
        print(out_txt)
        return json.loads(out_txt)['stories']
#        try:
#            return json.loads(out_txt)
#        except:
#            print(f"{out_txt}\nBad json? Retrying...")
