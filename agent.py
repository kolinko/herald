import openai

import os

import json
from common import json_fetch, ai, ai3, download_and_cache

from fetch import fetch_article

import tqdm
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates/"))
#template = environment.get_template("message.txt")

ISSUE_DAY = 16
ISSUE_MONTH = 5
ISSUE_YEAR = 2023

ISSUE = f"{ISSUE_YEAR}-{ISSUE_MONTH:02d}-{ISSUE_DAY:02d}"
ISSUE_FNAME = f"paper.{ISSUE}.json"

month_names = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May",
    6: "June", 7: "July", 8: "August", 9: "September",
    10: "October", 11: "November", 12: "December"}

def day_suffix(day):
    if 4 <= day <= 20 or 24 <= day <= 30:
        return "th"
    else:
        return ["st", "nd", "rd"][day % 10 - 1]

ISSUE_DATE = f"{ISSUE_DAY}<span style='font-size:15px'>{day_suffix(ISSUE_DAY)}</span>&nbsp;{month_names[ISSUE_MONTH]}&nbsp;{ISSUE_YEAR}"

title = "Hacker Herald"

def check_dir():
    if not os.path.exists(ISSUE):
        os.makedirs(ISSUE)

check_dir()

short_names = {
    'Felicity "Scoop" Sanders - Senior Reporter':'Scoop',
    'Chip "The Geek" Gallagher - Tech Expert':'The Geek',
    'Daphne "The Whisperer" Lane - Gossip Columnist':'The Whisperer',
    'Lenny "Deadline" Dawson - Staff Writer':'Deadline',
    'Father Wojciech "The Holy Scribe" Kowalski - Ethics Consultant':'Holy Scribe',
    'Olivia "The Dreamer" Thompson - Junior Reporter':'The Dreamer',
    'Dr. Benjamin "Nobel Scribe" Clarke - Science Columnist':'Nobel Scribe',   
    '''Betsy "The Oracle" O'Hara - Social Media Manager''':'The Oracle',
    '''Harvey "Clickbait" Carmichael - Editor-in-Chief''':'Harvey',
    '''Chuck "The Huckster" Malone - Gadget Guru & Marketing Mastermind''':'The Huckster'
}

journalists = {
    'Felicity "Scoop" Sanders - Senior Reporter':'''Felicity "Scoop" Sanders is known for her tenacious pursuit of breaking news stories. She will go to any lengths to uncover the truth, whether that means staking out tech conferences or posing as a janitor to infiltrate a secretive start-up. Her colleagues often joke that she has the instincts of a bloodhound. While her methods may be unorthodox, Felicity's investigative skills are unmatched and she often breaks major stories before anyone else.''',
    'Chip "The Geek" Gallagher - Tech Expert':'''A self-proclaimed tech whiz, Chip "The Geek" Gallagher is the office's go-to expert on all things related to gadgets and software. He is obsessed with the latest tech trends, always the first to buy and dissect new devices. With a mind like a steel trap, Chip can recall the specs of any product he's ever laid his hands on. He has a knack for translating complex tech jargon into digestible tidbits for the tabloid's readership.''',
    'Daphne "The Whisperer" Lane - Gossip Columnist':'''Daphne "The Whisperer" Lane is the office's gossip guru, with a sixth sense for unearthing the juiciest tidbits about the lives of tech industry titans. Skilled in the art of schmoozing, she is often found rubbing elbows with the who's who of Silicon Valley at exclusive parties and events. Daphne has a vast network of sources, ensuring she always has the inside scoop on the latest scandals and romances in the tech world.''',
    'Lenny "Deadline" Dawson - Staff Writer':'''Lenny "Deadline" Dawson is a seasoned staff writer who has perfected the art of churning out articles at lightning speed. He has an uncanny ability to crank out captivating stories just minutes before the final deadline, leaving his colleagues in awe of his time management skills. While his reporting may occasionally lack depth, Lenny's talent for witty wordplay and his keen eye for visuals ensure that his articles are always engaging.''',
    'Father Wojciech "The Holy Scribe" Kowalski - Ethics Consultant':'''Father Wojciech "The Holy Scribe" Kowalski is a devout Polish-Catholic priest who serves as the office's moral compass. He is committed to bringing a sense of godliness and righteousness to the tabloid's content, even in the face of sensationalism. Always dressed in his traditional priestly attire, Father Kowalski is a stern yet well-respected figure in the office. Though his colleagues often push the boundaries, he never wavers in his pursuit of ethical journalism, often sprinkling spiritual wisdom throughout the paper.''',
    'Olivia "The Dreamer" Thompson - Junior Reporter':'''Olivia "The Dreamer" Thompson is a young, overly ambitious journalist, fresh out of journalism school and eager to make a name for herself. She dreams of one day writing for the Wall Street Journal and gaining international fame by winning a Pulitzer Prize. Olivia constantly pushes herself to uncover groundbreaking stories, hoping to impress both her colleagues and the industry at large. Her relentless drive and optimism make her a force to be reckoned with in the editorial office.''',
    'Dr. Benjamin "Nobel Scribe" Clarke - Science Columnist':'''Dr. Benjamin "Nobel Scribe" Clarke is a journalist Nobel Prize laureate who brings a wealth of knowledge and prestige to the tabloid. Despite his illustrious background, he doesn't quite fit in with the rest of the staff, often struggling to find a balance between his journalistic integrity and the tabloid's sensationalist nature. However, the job pays the bills, so he does his best to adapt while still offering well-researched and informative science articles. His presence in the office serves as a constant reminder of the heights that journalism can reach.''',    
}

sm_managers = {
    'name':'''Betsy "The Oracle" O'Hara - Social Media Manager''',
    'bio':'''Betsy "The Oracle" O'Hara is the office's social media savant, skilled in the art of generating buzz on every platform from Twitter to TikTok. She knows what will go viral before it even happens, and her colleagues have learned to trust her instincts when it comes to crafting the perfect tweet or Instagram caption. Betsy's ability to turn any story into a shareable, likeable piece of content has played a major role in the tabloid's online success.'''
}

editor_in_chief = {
    'name':'''Harvey "Clickbait" Carmichael - Editor-in-Chief''',
    'bio':'''A seasoned journalist with a nose for scandal, Harvey "Clickbait" Carmichael has made a name for himself in the world of tech news with his unparalleled ability to turn even the smallest rumors into full-blown controversies. He started as a tech blogger and built his reputation on digging up dirt on tech giants. A master of sensational headlines, Harvey knows how to attract readers with his bold, eye-catching articles. Despite his questionable ethics, he maintains a vast network of industry insiders who supply him with the latest gossip.'''
}

marketer = {
    'name':'''Chuck "The Huckster" Malone - Gadget Guru & Marketing Mastermind''',
    'bio':'''Chuck "The Huckster" Malone is a sleazy, yet dimwitted marketing expert who specializes in concocting outrageous and unbelievable gadgets that he believes will captivate the readers. Despite his ineptitude, Chuck's wild imagination and unwavering confidence in his ludicrous inventions make him an oddly entertaining presence in the office. His articles showcasing bizarre and impractical products never fail to amuse, leaving readers wondering if he's a genius or simply a master of the absurd.'''
}

#env = Environment(loader=FileSystemLoader("templates/"))

def make_paper_fifth():
    with open(ISSUE_FNAME, 'r') as f:
        paper = json.loads(f.read())

    stories = paper['stories']
    story_template = env.get_template("story.html")

    for story in stories:
        story_html = story_template.render(story=story, title=story['title'], ISSUE_DATE=ISSUE_DATE)
        with open(f"{ISSUE}/{story['sources'][0]}.html", 'w') as f:
            f.write(story_html)

    ads_html = '<h2>Ads</h2>'
    for ad in paper['ads']:
        if 'name' not in ad: continue
        ads_html += "<h4>{}</h4>".format(ad['name'])
        if 'company' in ad:
            ads_html += "<h5>by {}</h5>".format(ad['company'])
        if 'description' in ad:
            ads_html += "{}<br>".format(ad['description'])
        if 'price' in ad:
            ads_html += "<b>price:</b>  {}<br>".format(ad['price'])
        ads_html += "<br>"

    index_template = env.get_template("index.html")
    html = index_template.render(title=title, ISSUE_DATE=ISSUE_DATE, editors_note=paper['editors_note'], stories=stories, ads_html=ads_html)

    with open(f'{ISSUE}/index.html', 'w') as f:
        f.write(html)

def make_paper_fourth():
    print('generating ads...')

    with open(ISSUE_FNAME, 'r') as f:
        paper = json.loads(f.read())

    stories = ''

    for story in paper['stories']:
        stories += '- '+ story['title'] + '\n'

    harvey_prompt = f'''
I'm writing a parody story about an editorial office of a tabloid paper covering tech news. 

The paper is titled "Hacker Herald", and it's based on Hacker News news.

You are:
{marketer['name']}
{marketer['bio']}

Your editor in chief is:
{editor_in_chief['name']}
{editor_in_chief['bio']}

Remember that this is a comedy/parody, so make everything factual, but hilariously over-tabloidy. Think comic-book narrative.

Reply in a following json form:'''+'''
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
    paper['ads'] = res

    with open(ISSUE_FNAME, 'w') as f:
        f.write(json.dumps(paper, indent=2))


def make_full_story(story):
    short_name = short_names[story['author']]
    name = story['author']
    bio = journalists[name]

    source_id = str(story['sources'][0])
    source = json_fetch('item', source_id)
#        print(json.dumps(source))

    story['source_url'] = source['url']
    status_dict[short_name] = f"fetching: {source['url'][:50]} ..."
    source_text = fetch_article(source['url']) # can fail if source url doesn't exist. should try other sources then

    if '==error' in source_text:
        print(source_text)

    harvey_prompt = f'''
I'm writing a parody story about an editorial office of a tabloid paper covering tech news. 

The paper is titled "Hacker Herald", and it's based on Hacker News news.

You are:
{name}
{bio}

Your editor in chief is:
{editor_in_chief['name']}
{editor_in_chief['bio']}

Remember that this is a comedy/parody, so make everything factual, but hilariously over-tabloidy. Think comic-book narrative.

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
        status_dict[short_name] = "writing article..."
        reply = ai(harvey_prompt, user_prompt + count)

        required_sections = 'title', 'lead', 'text'
        if any(f'==={s}' not in reply for s in required_sections):
            count += '\nremember about formatting'
            continue

        result = {}
        result['title'] = reply[len('===title '):reply.find('===lead')]
        result['lead'] = reply[reply.find('===lead')+len('===lead '):reply.find('===text')]
        result['text'] = reply[reply.find('===text')+len('===text '):]

    return result

import threading
status_dict = {}
import time

def get_full_story(story):
    status_dict[short_names[story['author']]] = 'working...'
    story['full_story'] = make_full_story(story)
    status_dict[short_names[story['author']]] = 'Done'
    return story

def make_paper_third(stories_items):
    with open(ISSUE_FNAME, 'r') as f:
        paper = json.loads(f.read())

    threads = []
    for story in paper['stories']:
        t = threading.Thread(target=get_full_story, args=(story,))
        t.start()
        threads.append(t)

    time.sleep(1)
    cursor_up_code = '\x1b[1A'
    clear_line_code = '\x1b[2K'
    while True:
        print("\n".join([f"{k}: {v}" for k, v in status_dict.items()]))
        time.sleep(1)  # Delay between updates
        if all(value == 'Done' for value in status_dict.values()):  # If all tasks are done
            break

        print((cursor_up_code + clear_line_code) * len(status_dict), end='\r')


    for t in threads:
        t.join()

    with open(ISSUE_FNAME, 'w') as f:
        f.write(json.dumps(paper, indent=2))


def make_paper_second():
    print("writing editors' note")
    with open(ISSUE_FNAME, 'r') as f:
        paper = json.loads(f.read())

    stories = ''
    for story in paper:
        stories += '- ' + story['title'] + '\n'

    harvey_prompt = f'''
I'm writing a parody story about an editorial office of a tabloid paper covering tech news. 

The paper is titled "Hacker Herald", and it's based on Hacker News news.

You are:
{editor_in_chief['name']}
{editor_in_chief['bio']}


Remember that this is a comedy/parody, so make everything factual, but hilariously over-tabloidy. Think comic-book narrative.
'''
    user_prompt = f'''
Your journalists delivered these stories for the day:

{stories}

Write a brief, two-paragraph editor's note that will fit the front page. The words of wisdom that will encourage your readers to read the rest :)
'''

    note = ai(harvey_prompt, user_prompt)

    paper = {
        'stories': paper,
        'editors_note': note,
    }

    with open(ISSUE_FNAME, 'w') as f:
        f.write(json.dumps(paper, indent=2))



def make_paper_first(stories):
    """ prepare a table of contents """
    print('Asking each journalist to choose a subject and write a title for their piece...')
    others = ''

    paper = []
    used_up = []

    for your_name in tqdm.tqdm(journalists):
        your_bio = journalists[your_name]

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
        paper.append(picked)

        print(json.dumps(result, indent=2))

        print('paper so far:')
        print(json.dumps(paper, indent=2))

    with open(ISSUE_FNAME, 'w') as f:
        f.write(json.dumps(paper, indent=2))


def choose_stories(your_name, your_bio, others, stories):
    print(f'Asking {your_name}...')

    harvey_prompt = f'''
I'm writing a parody story about an editorial office of a tabloid paper covering tech news, titled "Hacker Herald" 

Two characters in the story:

{editor_in_chief['name']}
{editor_in_chief['bio']}

You are:
{your_name}
{your_bio}

Remember that this is a comedy/parody, so make everything factual, but hilariously over-tabloidy. Think comic-book narrative.

If you get asked to write a story, choose one theme, don't merge various themes.

Reformat the reply to be in json:'''+'''
[{"why":(five words why this story fits your speciality), "title":..., "sources":[source_ids],"title":...},...]

Three titles max, three sources max per title.
'''

    user_prompt = "Harvey, leaning on your desk with an intense expression, demands, " +\
                  "We need a front-page story from you for the day. " +\
                  "Pick something from this list and whip up a headline that'll make our readers' jaws drop!\n\n" +\
                     others + "\n\n" +\
                     stories

    while True:
        out_txt = ai(harvey_prompt, user_prompt)
        try:
            return json.loads(out_txt)
        except:
            print(f"{out_txt}\nBad json? Retrying...")
