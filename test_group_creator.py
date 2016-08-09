# -*- coding: utf-8 -*-

def test_create_groups_returns_list():
    from student_group_creator import create_groups
    infile = "testinputlist"
    assert type(create_groups(infile, [1, 4])) == list

def test_create_groups_needs_good_params():
    from student_group_creator import create_groups
    infile = "testinputlist"
    assert create_groups(infile, [0, 4]) == []
