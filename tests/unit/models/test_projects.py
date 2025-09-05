from mailtrap.models.projects import ProjectParams


class TestProjectParams:
    def test_api_data_should_return_dict_with_all_props(self) -> None:
        entity = ProjectParams(name="test")
        assert entity.api_data == {"name": "test"}
