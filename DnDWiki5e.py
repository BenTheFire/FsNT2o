class DnDWikiReference:
    title: str
    url: str
    description: str

    def __init__(self, title: str, url: str, description: str):
        self.title = title
        self.url = url
        self.description = description


class SpellReference:
    spell_name: str
    source: str
    level: int
    school: str
    casting_time: str
    range: str
    components: str
    duration: str
    description_text: str
    # None if not present
    at_higher_levels: str


    def __init__(self, spell_name: str):
        self.spell_name = spell_name

    def __str__(self):
        return f"Spell Name: {self.spell_name}\n" \
               f"Source: {self.source}\n" \
               f"Level: {self.level}\n" \
               f"School: {self.school}\n" \
               f"Casting Time: {self.casting_time}\n" \
               f"Range: {self.range}\n" \
               f"Components: {self.components}\n" \
               f"Duration: {self.duration}\n" \
               f"Description: {self.description_text}" + \
                (f"\nAt Higher Levels: {self.at_higher_levels}" if self.at_higher_levels else "")


def get_dnd_wikidot_com_page() -> DnDWikiReference:
    return DnDWikiReference("DnD Wiki", "https://dnd5e.wikidot.com/", "DnD Wikidot")


def get_spell_data_from_web(url: str):
    import requests
    from bs4 import BeautifulSoup
    # url = "https://dnd5e.wikidot.com/spell:fireball"
    page = requests.get(url)  # get the page
    soup = BeautifulSoup(page.content, 'html.parser')  # parse the page
    html_scrape = soup.find(class_='main-content').get_text()  # get the text from the main-content class

    # multiple newlines to single newline
    while "\n\n" in html_scrape:
        html_scrape = html_scrape.replace("\n\n", "\n")

    # remove the first and last newlines
    html_scrape = html_scrape.strip()
    # split the string into a list of strings
    html_scrape = html_scrape.split("\n")

    # region - Cantrip Check
    is_cantrip = False
    if "cantrip" in html_scrape[2].lower():
        is_cantrip = True
    print("Is Cantrip: ", is_cantrip)
    # endregion

    # region - Spell Reference Creation
    spell_reference = SpellReference(html_scrape[0])
    spell_reference.source = html_scrape[1].split(":")[1].strip()

    if is_cantrip:
        spell_reference.level = 0
        spell_reference.school = html_scrape[2].split(" ")[0].strip().lower()
    else:
        spell_reference.level = int(html_scrape[2].split(" ")[0][0])
        spell_reference.school = html_scrape[2].split(" ")[1].strip().lower()

    spell_reference.casting_time = html_scrape[3].split(":")[1].strip()
    spell_reference.range = html_scrape[4].split(":")[1].strip()
    spell_reference.components = html_scrape[5].split(":")[1].strip()
    spell_reference.duration = html_scrape[6].split(":")[1].strip()
    spell_reference.description_text = html_scrape[7] + "\n" + html_scrape[8]
    if "At Higher Levels." in spell_reference.description_text:
        spell_reference.at_higher_levels = spell_reference.description_text.split("At Higher Levels.")[1]
        spell_reference.description_text = spell_reference.description_text.split("At Higher Levels.")[0]
    else:
        spell_reference.at_higher_levels = None
    # endregion

    return spell_reference


def dnd_wikidot_lookup_spell(search: str) -> SpellReference:
    search = search.replace(" ", "-").lower()
    url = f"https://dnd5e.wikidot.com/spell:{search}"
    return get_spell_data_from_web(url)


startup = ("Thanks for using the DnD Wiki 5e module."
           " This module is designed to help you look up spells from the DnD 5e Wikidot page.")
print(startup)
