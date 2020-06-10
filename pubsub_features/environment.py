def before_scenario(context, scenario):
    assert len(scenario.effective_tags) == 1, 'Unexpected scenario tags'
    context.scenario_tag = scenario.effective_tags[0]
