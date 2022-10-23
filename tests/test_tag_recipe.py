from project.recipe import *

def test_tag_does_not_exist(monkeypatch):
    monkeypatch.setattr("project.db.TagRepo.select_by_name", lambda x: None)

    res = add_tag_to_recipe("I-dont-exist", 123, 123)
    assert res == "Tag does not exist"

def test_cannot_modify_the_recipe(monkeypatch):
    monkeypatch.setattr("project.db.TagRepo.select_by_name", lambda x: (1, "A"))
    monkeypatch.setattr("project.db.RecipeRepo.select_by_id_and_author", lambda x, y: None)

    res = add_tag_to_recipe("A", 123, 123)
    assert res == "Cannot modify this recipe"

def test_duplicate_association(monkeypatch):
    monkeypatch.setattr("project.db.TagRepo.select_by_name", lambda x: (1, "A"))
    monkeypatch.setattr("project.db.RecipeRepo.select_by_id_and_author", lambda x, y: (1,))
    monkeypatch.setattr("project.db.RecipeTagRepo.insert_row", lambda x, y: 1 / 0)
    monkeypatch.setattr("project.db.RecipeTagRepo.check_exists", lambda x, y: True)

    res = add_tag_to_recipe("A", 2, 5)
    assert res == "Recipe already has tag"

def test_paranoid(monkeypatch):
    monkeypatch.setattr("project.db.TagRepo.select_by_name", lambda x: (1, "A"))
    monkeypatch.setattr("project.db.RecipeRepo.select_by_id_and_author", lambda x, y: (1,))
    monkeypatch.setattr("project.db.RecipeTagRepo.insert_row", lambda x, y: 1 / 0)
    monkeypatch.setattr("project.db.RecipeTagRepo.check_exists", lambda x, y: False)

    res = add_tag_to_recipe("A", 2, 5)
    assert res == "Unknown error occurred"

