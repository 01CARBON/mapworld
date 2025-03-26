"""

{'transitions': 
    [ 
        {'source': '(2, 3)', 'dest': '(2, 2)', 'trigger': 's'}, 
        {'source': '(2, 2)', 'dest': '(2, 3)', 'trigger': 'n'}, 
        {'source': '(2, 2)', 'dest': '(2, 1)', 'trigger': 's'}, 
        {'source': '(2, 1)', 'dest': '(2, 2)', 'trigger': 'n'}, 
        {'source': '(2, 1)', 'dest': '(3, 1)', 'trigger': 'e'}, 
        {'source': '(3, 1)', 'dest': '(2, 1)', 'trigger': 'w'}, 
        {'source': '(2, 1)', 'dest': '(2, 0)', 'trigger': 's'}, 
        {'source': '(2, 0)', 'dest': '(2, 1)', 'trigger': 'n'}, 
        {'source': '(3, 1)', 'dest': '(3, 0)', 'trigger': 's'}, 
        {'source': '(3, 0)', 'dest': '(3, 1)', 'trigger': 'n'}, 
        {'source': '(3, 0)', 'dest': '(2, 0)', 'trigger': 'w'}, 
        {'source': '(2, 0)', 'dest': '(3, 0)', 'trigger': 'e'}, 
        {'source': '(2, 0)', 'dest': '(1, 0)', 'trigger': 'w'}, 
        {'source': '(1, 0)', 'dest': '(2, 0)', 'trigger': 'e'}, 
        {'source': '(1, 0)', 'dest': '(0, 0)', 'trigger': 'w'}, 
        {'source': '(0, 0)', 'dest': '(1, 0)', 'trigger': 'e'}, 
        {'source': '(1, 0)', 'dest': '(1, 1)', 'trigger': 'n'}, 
        {'source': '(1, 1)', 'dest': '(1, 0)', 'trigger': 's'}, 
        {'source': '(0, 0)', 'dest': '(0, 1)', 'trigger': 'n'}, 
        {'source': '(0, 1)', 'dest': '(0, 0)', 'trigger': 's'}, 
        {'source': '(0, 1)', 'dest': '(1, 1)', 'trigger': 'e'}, 
        {'source': '(1, 1)', 'dest': '(0, 1)', 'trigger': 'w'}
    ], 
    
'nodes': 
    [
        {'base_type': 'outdoor', 'type': np.str_('newsstand__outdoor'), 'target': False, 'image': np.str_('https://www.ling.uni-potsdam.de/clembench/adk/images/ADE/training/urban/newsstand__outdoor/ADE_train_00013834.jpg'), 'id': (2, 3)}, 
        {'base_type': 'indoor', 'type': np.str_('reception'), 'target': False, 'image': np.str_('https://www.ling.uni-potsdam.de/clembench/adk/images/ADE/training/work_place/reception/ADE_train_00015715.jpg'), 'id': (2, 2)}, 
        {'base_type': 'indoor', 'type': np.str_('kitchen'), 'target': True, 'image': np.str_('https://www.ling.uni-potsdam.de/clembench/adk/images/ADE/training/home_or_hotel/kitchen/ADE_train_00010480.jpg'), 'id': (2, 1)}, 
        {'base_type': 'indoor', 'type': np.str_('restroom__indoor'), 'target': False, 'image': np.str_('https://www.ling.uni-potsdam.de/clembench/adk/images/ADE/training/work_place/restroom__indoor/ADE_train_00015838.jpg'), 'id': (3, 1)}, 
        {'base_type': 'indoor', 'type': np.str_('kitchen'), 'target': True, 'image': np.str_('https://www.ling.uni-potsdam.de/clembench/adk/images/ADE/training/home_or_hotel/kitchen/ADE_train_00010443.jpg'), 'id': (3, 0)}, 
        {'base_type': 'indoor', 'type': np.str_('bathroom'), 'target': True, 'image': np.str_('https://www.ling.uni-potsdam.de/clembench/adk/images/ADE/training/home_or_hotel/bathroom/ADE_train_00002626.jpg'), 'id': (2, 0)}, 
        {'base_type': 'indoor', 'type': np.str_('workroom'), 'target': False, 'image': np.str_('https://www.ling.uni-potsdam.de/clembench/adk/images/ADE/training/work_place/workroom/ADE_train_00020100.jpg'), 'id': (1, 0)}, 
        {'base_type': 'indoor', 'type': np.str_('home_office'), 'target': False, 'image': np.str_('https://www.ling.uni-potsdam.de/clembench/adk/images/ADE/training/home_or_hotel/home_office/ADE_train_00009390.jpg'), 'id': (0, 0)}, 
        {'base_type': 'indoor', 'type': np.str_('bathroom'), 'target': True, 'image': np.str_('https://www.ling.uni-potsdam.de/clembench/adk/images/ADE/training/home_or_hotel/bathroom/ADE_train_00003005.jpg'), 'id': (0, 1)}, 
        {'base_type': 'indoor', 'type': np.str_('workroom'), 'target': False, 'image': np.str_('https://www.ling.uni-potsdam.de/clembench/adk/images/ADE/training/work_place/workroom/ADE_train_00020100.jpg'), 'id': (1, 1)}
    ], 
'initial': '(2, 3)', 
'initial_type': np.str_('newsstand__outdoor')}
"""