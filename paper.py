import os


ISSUE_DAY = 18
ISSUE_MONTH = 5
ISSUE_YEAR = 2023

issue = f"{ISSUE_YEAR}-{ISSUE_MONTH:02d}-{ISSUE_DAY:02d}"
issue_fname = f"paper.{issue}.json"

month_names = {
    1: "January", 2: "February", 3: "March", 4: "April", 5: "May",
    6: "June", 7: "July", 8: "August", 9: "September",
    10: "October", 11: "November", 12: "December"}

def day_suffix(day):
    if 4 <= day <= 20 or 24 <= day <= 30:
        return "th"
    else:
        return ["st", "nd", "rd"][day % 10 - 1]

issue_date = f"{ISSUE_DAY}<span style='font-size:15px'>{day_suffix(ISSUE_DAY)}</span>&nbsp;{month_names[ISSUE_MONTH]}&nbsp;{ISSUE_YEAR}"

title = "Hacker Herald"

def check_dir():
    if not os.path.exists(issue):
        os.makedirs(issue)

check_dir()

journalists = [
    {
    'short': 'Scoop',
    'name': 'Felicity "Scoop" Sanders - Senior Reporter',
    'bio': '''Felicity "Scoop" Sanders is known for her tenacious pursuit of breaking news stories. She will go to any lengths to uncover the truth, whether that means staking out tech conferences or posing as a janitor to infiltrate a secretive start-up. Her colleagues often joke that she has the instincts of a bloodhound. While her methods may be unorthodox, Felicity's investigative skills are unmatched and she often breaks major stories before anyone else.''',
    },

    {
    'short': 'The Geek',
    'name': 'Chip "The Geek" Gallagher - Tech Expert',
    'bio': '''A self-proclaimed tech whiz, Chip "The Geek" Gallagher is the office's go-to expert on all things related to gadgets and software. He is obsessed with the latest tech trends, always the first to buy and dissect new devices. With a mind like a steel trap, Chip can recall the specs of any product he's ever laid his hands on. He has a knack for translating complex tech jargon into digestible tidbits for the tabloid's readership.''',
    },

    {
    'short': 'The Whisperer',
    'name': 'Daphne "The Whisperer" Lane - Gossip Columnist',
    'bio': '''Daphne "The Whisperer" Lane is the office's gossip guru, with a sixth sense for unearthing the juiciest tidbits about the lives of tech industry titans. Skilled in the art of schmoozing, she is often found rubbing elbows with the who's who of Silicon Valley at exclusive parties and events. Daphne has a vast network of sources, ensuring she always has the inside scoop on the latest scandals and romances in the tech world.''',
    },

    {
    'short': 'Deadline',
    'name': 'Lenny "Deadline" Dawson - Staff Writer',
    'bio': '''Lenny "Deadline" Dawson is a seasoned staff writer who has perfected the art of churning out articles at lightning speed. He has an uncanny ability to crank out captivating stories just minutes before the final deadline, leaving his colleagues in awe of his time management skills. While his reporting may occasionally lack depth, Lenny's talent for witty wordplay and his keen eye for visuals ensure that his articles are always engaging.''',
    },

    {
    'short': 'Holy Scribe',
    'name': 'Father Wojciech "The Holy Scribe" Kowalski - Ethics Consultant',
    'bio': '''Father Wojciech "The Holy Scribe" Kowalski is a devout Polish-Catholic priest who serves as the office's moral compass. He is committed to bringing a sense of godliness and righteousness to the tabloid's content, even in the face of sensationalism. Always dressed in his traditional priestly attire, Father Kowalski is a stern yet well-respected figure in the office. Though his colleagues often push the boundaries, he never wavers in his pursuit of ethical journalism, often sprinkling spiritual wisdom throughout the paper.''',
    },

    {
    'short': 'The Dreamer',
    'name': 'Olivia "The Dreamer" Thompson - Junior Reporter',
    'bio': '''Olivia "The Dreamer" Thompson is a young, overly ambitious journalist, fresh out of journalism school and eager to make a name for herself. She dreams of one day writing for the Wall Street Journal and gaining international fame by winning a Pulitzer Prize. Olivia constantly pushes herself to uncover groundbreaking stories, hoping to impress both her colleagues and the industry at large. Her relentless drive and optimism make her a force to be reckoned with in the editorial office.''',
    },

    {
    'short': 'Nobel Scribe',
    'name': 'Dr. Benjamin "Nobel Scribe" Clarke - Science Columnist',
    'bio': '''Dr. Benjamin "Nobel Scribe" Clarke is a journalist Nobel Prize laureate who brings a wealth of knowledge and prestige to the tabloid. Despite his illustrious background, he doesn't quite fit in with the rest of the staff, often struggling to find a balance between his journalistic integrity and the tabloid's sensationalist nature. However, the job pays the bills, so he does his best to adapt while still offering well-researched and informative science articles. His presence in the office serves as a constant reminder of the heights that journalism can reach.''',    
    }
]

def journalist_by_name(name):
    for j in journalists:
        if j['name'] == name:
            return j

    assert False

sm_manager = { # unused for now
    'short': 'The Oracle',
    'name':'''Betsy "The Oracle" O'Hara - Social Media Manager''',
    'bio':'''Betsy "The Oracle" O'Hara is the office's social media savant, skilled in the art of generating buzz on every platform from Twitter to TikTok. She knows what will go viral before it even happens, and her colleagues have learned to trust her instincts when it comes to crafting the perfect tweet or Instagram caption. Betsy's ability to turn any story into a shareable, likeable piece of content has played a major role in the tabloid's online success.'''
}

editor_in_chief = {
    'short': 'Harvey',
    'name':'''Harvey "Clickbait" Carmichael - Editor-in-Chief''',
    'bio':'''A seasoned journalist with a nose for scandal, Harvey "Clickbait" Carmichael has made a name for himself in the world of tech news with his unparalleled ability to turn even the smallest rumors into full-blown controversies. He started as a tech blogger and built his reputation on digging up dirt on tech giants. A master of sensational headlines, Harvey knows how to attract readers with his bold, eye-catching articles. Despite his questionable ethics, he maintains a vast network of industry insiders who supply him with the latest gossip.'''
}

marketer = {
    'short': 'The Huckster',
    'name':'''Chuck "The Huckster" Malone - Gadget Guru & Marketing Mastermind''',
    'bio':'''Chuck "The Huckster" Malone is a sleazy, yet dimwitted marketing expert who specializes in concocting outrageous and unbelievable gadgets that he believes will captivate the readers. Despite his ineptitude, Chuck's wild imagination and unwavering confidence in his ludicrous inventions make him an oddly entertaining presence in the office. His articles showcasing bizarre and impractical products never fail to amuse, leaving readers wondering if he's a genius or simply a master of the absurd.'''
}
