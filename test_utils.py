import pytest
import utils

# Необязательное задание - тест для функции нахождения актеров-партнеров


params = [('Rose McIver', 'Ben Lamb', ['Alice Krige', 'Honor Kneafsey']),
          ('Jack Black', 'Dustin Hoffman', ['David Cross', 'Seth Rogen'])]

exceptions_params = [
    (1, '2', TypeError),
    ('Nick', 0.5, TypeError),
    (45, [], TypeError),
    ((2, 6), 'Jack', TypeError),
    ({}, (), TypeError)
]


class TestSearchForFellowActors:
    def test_result_type(self):
        result = utils.search_for_fellow_actors(utils.database, 'Rose McIver', 'Ben Lamb')
        assert isinstance(result, list) is True, 'Возвращает не список'

    def test_nonexistient_actors(self):
        result = utils.search_for_fellow_actors(utils.database, 'Ms. Nobody', 'J. Somebody')
        assert isinstance(result, list) is True, 'Возвращает не список'
        assert len(result) == 0, 'Возвращает непустой список'

    @pytest.mark.parametrize("first_actor, second_actor, expected", params)
    def test_search_for_fellow_actors(self, first_actor, second_actor, expected):
        result = utils.search_for_fellow_actors(utils.database, first_actor, second_actor)
        assert result == expected, 'Возвращает некорректных актеров'

    @pytest.mark.parametrize("first_actor, second_actor, exception", exceptions_params)
    def test_type_errors(self, first_actor, second_actor, exception):
        with pytest.raises(exception):
            assert utils.search_for_fellow_actors(utils.database, first_actor, second_actor)


