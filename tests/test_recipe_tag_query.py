from project.recipe_query import *
from project.tag_query import *

def gen_scenario_helper():
    recipes_with_tags = [
        # id title          body                               author               tags
        (1,  "Good recipe", "This is a good recipe",           "Someone Somewhere", [1]),
        (2,  "A recipe",    "This is a random recipe",         "Another Person",    [3]),
        (3,  "Wow food",    "Insane recipe never seen before", "Person Guy",        [1, 2])
    ]

    tags = [
        # id title
        (1,  "vegan"),
        (2,  "gluten-free"),
        (3,  "healthy")
    ]

    def select_many_filtered(title, tags=[], offset=0, limit=None):
        # this is quite the complex stub...

        import re
        tags = set(tags)
        filtered = [ent for ent in recipes_with_tags if re.search(title, ent[1]) and tags <= set(ent[4])]

        if not limit:
            return filtered[offset:]
        return filtered[offset:offset+limit]

    def select_all():
        return tags

    def select_by_names(names):
        return [ent for ent in tags if ent[1] in names]

    return (select_many_filtered, select_all, select_by_names)

def test_scenario_Search_a_recipe_by_name(monkeypatch):
    """
    When searching for recipes with the query string "Good recipe"
    Then the following list of recipes is returned:
    | recipe_id  | recipe_author      | recipe_title  | recipe_body                     |
    | 1          | Someone Somewhere  | Good recipe   | This is a good recipe           |

    """

    (select_many_filtered, select_all, select_by_names) = gen_scenario_helper()
    monkeypatch.setattr("project.db.RecipeRepo.select_many_filtered", select_many_filtered)
    monkeypatch.setattr("project.db.TagRepo.select_all", select_all)
    monkeypatch.setattr("project.db.TagRepo.select_by_names", select_by_names)

    (res, err) = search_recipes_by_filter("Good recipe", [], 0)
    assert err is None
    assert len(res) == 1

    assert res[0][0] == 1
    assert res[0][1] == "Good recipe"
    assert res[0][2] == "This is a good recipe"
    assert res[0][3] == "Someone Somewhere"

def test_scenario_Search_for_a_term_matching_multiple_recipes(monkeypatch):
    """
    When searching for recipes with the query string "recipe"
    Then the following list of recipes is returned:
    | recipe_id  | recipe_author      | recipe_title  | recipe_body                     |
    | 1          | Someone Somewhere  | Good recipe   | This is a good recipe           |
    | 2          | Another Person     | A recipe      | This is a random recipe         |
    """

    (select_many_filtered, select_all, select_by_names) = gen_scenario_helper()
    monkeypatch.setattr("project.db.RecipeRepo.select_many_filtered", select_many_filtered)
    monkeypatch.setattr("project.db.TagRepo.select_all", select_all)
    monkeypatch.setattr("project.db.TagRepo.select_by_names", select_by_names)

    (res, err) = search_recipes_by_filter("recipe", [], 0)
    assert err is None
    assert len(res) == 2

    assert res[0][0] == 1
    assert res[0][1] == "Good recipe"
    assert res[0][2] == "This is a good recipe"
    assert res[0][3] == "Someone Somewhere"

    assert res[1][0] == 2
    assert res[1][1] == "A recipe"
    assert res[1][2] == "This is a random recipe"
    assert res[1][3] == "Another Person"

def test_scenario_Search_for_recipes_with_invalid_search_parameter(monkeypatch):
    """
    When searching for recipes with the query string " "
    Then the following list of recipes is returned:
    | recipe_id  | recipe_author      | recipe_title  | recipe_body                     |

    """

    (select_many_filtered, select_all, select_by_names) = gen_scenario_helper()
    monkeypatch.setattr("project.db.RecipeRepo.select_many_filtered", select_many_filtered)
    monkeypatch.setattr("project.db.TagRepo.select_all", select_all)
    monkeypatch.setattr("project.db.TagRepo.select_by_names", select_by_names)

    (res, err) = search_recipes_by_filter(" ", [], 0)
    assert err is None
    assert len(res) == 0

def test_scenario_Query_all_possible_tags(monkeypatch):
    """
    When the user requests the list of all possible tags
    Then the the system returns the following list of tags:
    | tag_id | tag title   |
    | 1      | vegan       |
    | 2      | gluten-free |
    | 3      | healthy     |
    """

    (select_many_filtered, select_all, select_by_names) = gen_scenario_helper()
    monkeypatch.setattr("project.db.RecipeRepo.select_many_filtered", select_many_filtered)
    monkeypatch.setattr("project.db.TagRepo.select_all", select_all)
    monkeypatch.setattr("project.db.TagRepo.select_by_names", select_by_names)

    res = get_all_tags()
    assert res == [(1, "vegan"), (2, "gluten-free"), (3, "healthy")]

def test_scenario_Filter_a_recipe_by_tag(monkeypatch):
    """
    When attempting to filter recipes with the tag "vegan"
    Then the following list of recipes is returned:
    | recipe_id  | recipe_author      | recipe_title  | recipe_body                     |
    | 1          | Someone Somewhere  | Good recipe   | This is a good recipe           |
    | 3          | Person Guy         | Wow food      | Insane recipe never seen before |
    """

    (select_many_filtered, select_all, select_by_names) = gen_scenario_helper()
    monkeypatch.setattr("project.db.RecipeRepo.select_many_filtered", select_many_filtered)
    monkeypatch.setattr("project.db.TagRepo.select_by_names", select_by_names)

    (res, err) = search_recipes_by_filter("", ["vegan"], 0)
    assert err is None
    assert len(res) == 2

    assert res[0][0] == 1
    assert res[0][1] == "Good recipe"
    assert res[0][2] == "This is a good recipe"
    assert res[0][3] == "Someone Somewhere"

    assert res[1][0] == 3
    assert res[1][1] == "Wow food"
    assert res[1][2] == "Insane recipe never seen before"
    assert res[1][3] == "Person Guy"

def test_scenario_Filter_a_recipe_with_multiple_tags(monkeypatch):
    """
    When attempting to filter recipes with the tags "vegan" and "gluten-free"
    Then the following list of recipes is returned:
    | recipe_id  | recipe_author      | recipe_title  | recipe_body                     |
    | 3          | Person Guy         | Wow food      | Insane recipe never seen before |
    """

    (select_many_filtered, select_all, select_by_names) = gen_scenario_helper()
    monkeypatch.setattr("project.db.RecipeRepo.select_many_filtered", select_many_filtered)
    monkeypatch.setattr("project.db.TagRepo.select_all", select_all)
    monkeypatch.setattr("project.db.TagRepo.select_by_names", select_by_names)

    (res, err) = search_recipes_by_filter("", ["vegan", "gluten-free"], 0)
    assert err is None
    assert len(res) == 1

    assert res[0][0] == 3
    assert res[0][1] == "Wow food"
    assert res[0][2] == "Insane recipe never seen before"
    assert res[0][3] == "Person Guy"

def test_scenario_Filter_a_recipe_by_tags_and_search_for_title(monkeypatch):
    """
    When attempting to filter recipes with the tag "vegan" and search parameter "recipe"
    Then the following list of recipes is returned:
    | recipe_id  | recipe_author      | recipe_title  | recipe_body                     |
    | 1          | Someone Somewhere  | Good recipe   | This is a good recipe           |
    """

    (select_many_filtered, select_all, select_by_names) = gen_scenario_helper()
    monkeypatch.setattr("project.db.RecipeRepo.select_many_filtered", select_many_filtered)
    monkeypatch.setattr("project.db.TagRepo.select_all", select_all)
    monkeypatch.setattr("project.db.TagRepo.select_by_names", select_by_names)

    (res, err) = search_recipes_by_filter("recipe", ["vegan"], 0)
    assert err is None
    assert len(res) == 1

    assert res[0][0] == 1
    assert res[0][1] == "Good recipe"
    assert res[0][2] == "This is a good recipe"
    assert res[0][3] == "Someone Somewhere"

def test_scenario_Filter_a_recipe_with_invalid_tag(monkeypatch):
    """
    When attempting to filter recipes with the tag "apoplexy-inducing"
    Then the "This tag does not exist" error message is issued
    """

    (select_many_filtered, select_all, select_by_names) = gen_scenario_helper()
    monkeypatch.setattr("project.db.RecipeRepo.select_many_filtered", select_many_filtered)
    monkeypatch.setattr("project.db.TagRepo.select_all", select_all)
    monkeypatch.setattr("project.db.TagRepo.select_by_names", select_by_names)

    (res, err) = search_recipes_by_filter("", ["apoplexy-inducing"], 0)
    assert res is None
    assert err == "This tag does not exist"

def test_scenario_Filter_a_recipe_with_multiple_tags_one_of_which_is_invalid(monkeypatch):
    """
    When attempting to filter recipes with the tags "vegan" and "100% organic certified"
    Then the "This tag does not exist" error message is issued
    """

    (select_many_filtered, select_all, select_by_names) = gen_scenario_helper()
    monkeypatch.setattr("project.db.RecipeRepo.select_many_filtered", select_many_filtered)
    monkeypatch.setattr("project.db.TagRepo.select_all", select_all)
    monkeypatch.setattr("project.db.TagRepo.select_by_names", select_by_names)

    (res, err) = search_recipes_by_filter("", ["vegan", "100% organic certified"], 0)
    assert res is None
    assert err == "This tag does not exist"

