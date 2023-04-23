import openai

from api_keys import organisation, api_key
openai.organization = organisation
openai.api_key = api_key

import json
from common import json_fetch

from fetch import fetch_text

def ai(system, prompt):
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": prompt}
    ]
    completion = openai.ChatCompletion.create(model="gpt-4", messages=messages)
    return completion.choices[0].message.content


title = "Hacker Herald"

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

def make_paper(_):
    with open('paper.json', 'r') as f:
        paper = json.loads(f.read())

    stories_html = ''

    for story in paper['stories']:
        story_html = '''<!DOCTYPE html>
<html lang="en">

<link href="https://fonts.googleapis.com/css2?family=Georgia&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">

<style>
body {
    font-family: Verdana, Geneva, sans-serif, "Roboto", Arial, sans-serif;
    font-size: 16px;
    line-height: 2;
    color: #333;
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
}

td {
    font-family: "Playfair Display", Times, serif;
    font-size:30px;    
}

h1 {
    font-family: "Playfair Display", Times, serif;

    font-size: 48px;
    margin-bottom: 0px;
    font-weight: bold;
}

h2 {
    font-family: "Georgia", Times, serif;

    font-size: 36px;
    margin-bottom: 10px;
    font-weight: bold;
}

h5, h4 {
    margin-top:0px;
    margin-bottom:0px;

}

a {
    font-family: "Georgia", Times, serif;

    color: #1a1a1a;
    text-decoration: none;
    font-weight: bold;
}

a:hover {
    color: #0000ff;
}

.ads-section {
    margin-top: 20px;
}

h3 {
    font-family: "Georgia", Times, serif;
    font-size: 18px;
    font-weight: bold;
    text-align: left;
    margin-bottom: 20px;
}

dd {
    margin-bottom:20px;
}
dt{
    font-weight:bold;
}
</style>'''+f'''
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{story['title']}</title>
</head>
<body>
  <h1>Hacker Herald</h1>

  <article>
    <h2>{story['title']}</h2>
    <p><em>By {story['author']}</em></p>
    <p><strong>Date:</strong> 23 Apr 2023</p>
    <b><i>{story['full_story']['lead']}</b></i>
    <p>{story['full_story']['text']}</p>
  </article>
</body>
</html>'''

        with open(f"{story['sources'][0]}_.html", 'w') as f:
            f.write(story_html)

    exit()

    for story in paper['stories']:
        stories_html += f'''
            <a href="id">{story['title']}</a><br>
            {story['full_story']['lead']}<br>
        '''

    ads_html = ''

    for ad in paper['ads']:
        ads_html += f'''
    <h4>{ad['name']}</h4>
    <h5>by {ad['company']}</h5>
    {ad['description']}<br>
    price:  {ad['price']}<br><br>
        '''


    editors_note = paper['editors_note'].replace('\n', '<br>')

    html = f'''
<head>
<body>
<h1>{title}</h1>
<h2>Editor's note</h2>
{editors_note}
<h2>Today's stories</h2>
{stories_html}
<h2>Ads</h2>
{ads_html}
</body>
</html>
    '''

    with open('index_tmp.html', 'w') as f:
        f.write(html)
    exit()

def make_paper_fourth(_):
    with open('paper.json', 'r') as f:
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
    print(res)
    res = json.loads(res)
    paper['ads'] = res

    with open('paper.json', 'w') as f:
        f.write(json.dumps(paper, indent=2))

    exit()

def make_paper_third(stories_items):
    with open('paper.json', 'r') as f:
        paper = json.loads(f.read())

    for story in paper['stories']:
        name = story['author']
        bio = journalists[name]

        source_id = str(story['sources'][0])
        source = json_fetch('item', source_id)
#        print(json.dumps(source))

        story['source_url'] = source['url']
        source_text = fetch_text(source['url']) # can fail if source url doesn't exist. should try other sources then

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

#        print()
#        print(harvey_prompt)
#        print('#####\n\n\n')
#        print(user_prompt)

        print(f'Asking {name}...')

        result = None
        count=''

        while result is None:

            reply = ai(harvey_prompt, user_prompt+count)

            if '===title' not in reply:
                count += '\nremember about formatting'
                continue

            if '===lead' not in reply:
                count += '\nremember about formatting'
                continue

            if '===text' not in reply:
                count += '\nremember about formatting'
                continue

            print(reply)

            result = {}
            result['title'] = reply[len('===title '):reply.find('===lead')]
            result['lead'] = reply[reply.find('===lead')+len('===lead '):reply.find('===text')]
            result['text'] = reply[reply.find('===text')+len('===text '):]

            story['full_story'] = result


    with open('paper.json', 'w') as f:
        f.write(json.dumps(paper, indent=2))



def make_paper_second(_):
    with open('paper.json', 'r') as f:
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

    with open('paper.json', 'w') as f:
        f.write(json.dumps(paper, indent=2))


def make_stories(your_name, your_bio, others, stories):
    print(f'asking {your_name}')

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
[{"title":..., "sources":[source_ids]},{"title":...}]

Three titles max, three sources max per title.
'''

    user_prompt = f"""Harvey, leaning on your desk with an intense expression, demands, "We need a front-page story from you for the day. Pick something from this list and whip up a headline that'll make our readers' jaws drop!

{others}

{stories}

"""

    result = ai(harvey_prompt, user_prompt)
    return result


def make_paper_first(stories):
    """ prepare a table of contents """

    others = ''

    paper = []

    for your_name in journalists:
        your_bio = journalists[your_name]

        result = None
        while result is None:
            out_txt = make_stories(your_name, your_bio, others, stories)
            try:
                result = json.loads(out_txt)
            except:
                print(f"{out}\nbad json? retrying")
  
        # TODO: make Harvey choose the best story

        picked = result[0]

        if others == '':
            others = 'Others already took these stories, so pick something else than them:\n'
        
        others += picked['title'] + '\n'
        picked['author'] = your_name
        paper.append(picked)

        print(json.dumps(result, indent=2))

        print('paper so far:')
        print(json.dumps(paper, indent=2))

    with open('paper.json', 'w') as f:
        f.write(json.dumps(paper, indent=2))

#        exit()

