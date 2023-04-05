from project import check_sys_args, collect_input, get_drink_recipe
import pytest


def test_check_sys_args():
    # correct usage
    assert(check_sys_args(['project.py', 'utils/test_input/diagonal.txt'], 2)) == 1
    assert(check_sys_args(['project.py', 'utils/test_input/row.csv'], 2)) == 1

    # not enough arguments
    with pytest.raises(SystemExit) as e:
        check_sys_args(['project.py'], 1)
    assert e.type == SystemExit

    # wrong file extension
    with pytest.raises(SystemExit) as e:
        check_sys_args(['project.py', 'a_pdf.pdf'], 2)
    assert e.type == SystemExit

    # file doesn't exist
    with pytest.raises(SystemExit) as e:
        check_sys_args(['project.py', 'file_that_doesnt_exist.txt'], 2)
    assert e.type == SystemExit


def test_collect_input():
    # test with provided input files
    assert(collect_input('utils/test_input/diagonal.txt')) == ['gin_tonic', 'gin_fizz', 'negroni', 'planter’s_punch', 'rändom']
    assert(collect_input('utils/test_input/diagonal.csv')) == ['gin_tonic', 'gin_fizz', 'negroni', 'planter’s_punch', 'random']
    assert(collect_input('utils/test_input/row.csv')) == ['random', 'gin_tonic']
    assert(collect_input('utils/test_input/row.txt')) == ['random', 'gin_tonic']
    

def test_get_drink_recipe():
    # test for the correct keys since the image name is random
    assert(list(get_drink_recipe('gin_tonic').keys())) == ['name', 'instructions', 'glass', 'ingredient1', 'measure1', 'ingredient2', 'measure2', 'ingredient3', 'measure3', 'ingredient4', 'measure4', 'image']
    assert(list(get_drink_recipe('negroni').keys())) == ['name', 'instructions', 'glass', 'ingredient1', 'measure1', 'ingredient2', 'measure2', 'ingredient3', 'measure3', 'image']

