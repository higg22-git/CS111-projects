from byu_pytest_utils import max_score, run_python_script, test_files, this_folder, with_import, ensure_missing
from pytest import approx
import pytest
from byuimage import Image
import matplotlib.pyplot as plt
import requests
from unittest.mock import patch


def do_invalid_args_test(capsys, error_message='', *args):
    try:
        run_python_script(str(this_folder / 'webcrawler.py'), *args)
    except SystemExit:
        pass  # ignore any exceptions
    captured = capsys.readouterr()
    assert 'invalid arguments' in captured.out.lower(), f"Your program didn't print 'invalid arguments' with command line arguments {args}. {error_message}"

# # MY TESTS
# from webcrawler import verify_prompt

# def test_verify_prompt():
#     assert verify_prompt('-c', 'https://byu.edu', 'out.txt', 'otherout.txt') == True
#     assert verify_prompt('-p', 'https://byu.edu', 'out.txt', 'otherout.txt') == True
#     assert verify_prompt('-i', 'https://byu.edu', 'out.txt', '-g') == True
#     assert verify_prompt('-i', 'https://byu.edu', 'out.txt', 'output.txt') == ValueError('invalid arguments')
#     assert verify_prompt('-i', 'http://byu.edu', 'out.txt', 'output.txt') == ValueError('invalid arguments')





@max_score(10)
def test_invalid_arguments(capsys):
    do_invalid_args_test(capsys, "Invalid due to no flag.")
    do_invalid_args_test(capsys, "Invalid due to invalid flag.",
                         'asdf')
    do_invalid_args_test(capsys, "Invalid due to invalid flag.",
                         '-a')
    do_invalid_args_test(capsys, "Invalid due to not enough arguments.",
                         '-c')
    do_invalid_args_test(capsys, "Invalid due to not enough arguments.",
                         '-c', 'https://cs111.byu.edu/')
    do_invalid_args_test(capsys, "Invalid due to not enough arguments.",
                         '-p')
    do_invalid_args_test(capsys, "Invalid due to not enough arguments.",
                         '-p', 'https://cs111.byu.edu/')
    do_invalid_args_test(capsys, "Invalid due to not enough arguments.",
                         '-i')
    do_invalid_args_test(capsys, "Invalid due to not enough arguments.",
                         '-i', 'https://cs111.byu.edu/')
    do_invalid_args_test(capsys, "Invalid because '-a' is not a valid image flag.",
                         '-i', 'https://cs111.byu.edu/', 'asdf_', '-a')


@pytest.fixture(scope="session")
@with_import('RequestGuard', 'RequestGuard')
def request_guard_tests(RequestGuard):
    try:
        guard = RequestGuard('https://cs111.byu.edu')
        # Mocking a different robots.txt
        guard.forbidden = ["/data", "/images/jpg", "/Projects/Project4/Project4.md"]

        assert     guard.can_follow_link('https://cs111.byu.edu/')
        assert     guard.can_follow_link('https://cs111.byu.edu/asdf.html')
        assert     guard.can_follow_link('https://cs111.byu.edu/Projects/Project4/')
        assert     guard.can_follow_link('https://cs111.byu.edu/Projects/Project4/Project3.md')
        assert     guard.can_follow_link('https://cs111.byu.edu/images/asdf.jpg')
        assert     guard.can_follow_link('https://cs111.byu.edu/images/png/asdf.png')
        assert not guard.can_follow_link('https://byu.edu/')
        assert not guard.can_follow_link('https://cs111.byu.edu/data/')
        assert not guard.can_follow_link('https://cs111.byu.edu/data/asdf.csv')
        assert not guard.can_follow_link('https://cs111.byu.edu/images/jpg/')
        assert not guard.can_follow_link('https://cs111.byu.edu/images/jpg/asdf.jpg')
        assert not guard.can_follow_link('https://cs111.byu.edu/Projects/Project4/Project4.md')


        guard = RequestGuard("https://cs111.byu.edu/Homework/homework07/")
        # Mocking a different robots.txt
        guard.forbidden = ['/data', '/images/jpg', '/lectures/Stephens']
        assert     guard.can_follow_link('https://cs111.byu.edu/')
        assert     guard.can_follow_link('https://cs111.byu.edu/asdf.html')
        assert     guard.can_follow_link('https://cs111.byu.edu/Projects/Project4/')
        assert     guard.can_follow_link('https://cs111.byu.edu/lectures/Reynolds/')
        assert     guard.can_follow_link('https://cs111.byu.edu/images/asdf.jpg')
        assert     guard.can_follow_link('https://cs111.byu.edu/images/png/asdf.png')
        assert not guard.can_follow_link('https://byu.edu/')
        assert not guard.can_follow_link('https://cs111.byu.edu/data/')
        assert not guard.can_follow_link('https://cs111.byu.edu/data/asdf.csv')
        assert not guard.can_follow_link('https://cs111.byu.edu/images/jpg/')
        assert not guard.can_follow_link('https://cs111.byu.edu/images/jpg/asdf.jpg')
        assert not guard.can_follow_link('https://cs111.byu.edu/lectures/Stephens/')


        assert RequestGuard('https://cs111.byu.edu').forbidden == ['/Projects/project04/assets/page5.html']
        assert RequestGuard('https://cs111.byu.edu/Homework/homework07/').forbidden == ['/Projects/project04/assets/page5.html']
    except Exception as e:
        return e


@max_score(15)
def test_request_guard(request_guard_tests):
    if type(request_guard_tests) == Exception:
        raise request_guard_tests


def assert_equal(observed: Image, expected: Image):
    assert observed.width == expected.width
    assert observed.height == expected.height
    for y in range(observed.height):
        for x in range(observed.width):
            observed_pixel = observed.get_pixel(x, y)
            expected_pixel = expected.get_pixel(x, y)
            assert observed_pixel.red == approx(expected_pixel.red, abs=1.1), f"The pixels' red values at ({x}, {y}) don't match. Expected `{expected_pixel.red}`, but got `{observed_pixel.red}`."
            assert observed_pixel.green == approx(expected_pixel.green, abs=1.1), f"The pixels' green values at ({x}, {y}) don't match. Expected `{expected_pixel.green}`, but got `{observed_pixel.green}`."
            assert observed_pixel.blue == approx(expected_pixel.blue, abs=1.1), f"The pixels' blue values at ({x}, {y}) don't match. Expected `{expected_pixel.blue}`, but got `{observed_pixel.blue}`."


def check_output_file(output_file, expected_file):
    try:
        with open(output_file, 'r') as out_file, open(expected_file, 'r') as expect_file:
                assert out_file.read() == expect_file.read(), "Output file does not match expected file"
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Couldn't find the output file: {e}")


def create_safe_request(max_requests=50):
    request_count = 0
    original_get = requests.get

    def safe_request(url, stream=False):
        nonlocal request_count
        request_count += 1
        if request_count > max_requests:
            raise InterruptedError(f"Program tried making too many GET requests ({max_requests}). Aborting tests.")
        if not url.startswith("https://cs111.byu.edu"):
            raise ConnectionError(f"Tried to request non BYU url: {url}")
        return original_get(url, stream=stream)

    return safe_request


@ensure_missing(this_folder / 'count_links.output.csv')
@ensure_missing(this_folder / 'count_links.output.png')
@max_score(25)
@patch('requests.get', create_safe_request(max_requests=10))
def test_count_links(request_guard_tests):
    if type(request_guard_tests) == Exception:
        assert False, 'RequestGuard must work before the rest of the assignment can be tested'

    plt.clf()
    run_python_script(
        this_folder / 'webcrawler.py', '-c',
        'https://cs111.byu.edu/Projects/project04/assets/page1.html',
        this_folder / 'count_links.output.png',
        this_folder / 'count_links.output.csv'
    )

    observed = Image(this_folder / 'count_links.output.png')
    expected = Image(test_files / 'count_links.key.png')
    assert_equal(observed, expected)

    check_output_file(this_folder / 'count_links.output.csv', test_files / 'count_links.key.csv')


@ensure_missing(this_folder / 'plot_data.output.png')
@ensure_missing(this_folder / 'plot_data.output.csv')
@max_score(12.5)
@patch('requests.get', create_safe_request(max_requests=5))
def test_plot_data_two_column(request_guard_tests):
    if type(request_guard_tests) == Exception:
        assert False, 'RequestGuard must work before the rest of the assignment can be tested'

    plt.clf()
    run_python_script(
        this_folder / 'webcrawler.py', '-p',
        'https://cs111.byu.edu/Projects/project04/assets/data.html',
        this_folder / 'plot_data.output.png',
        this_folder / 'plot_data.output.csv'
    )

    observed = Image(this_folder / 'plot_data.output.png')
    expected = Image(test_files / 'plot_data.key.png')
    assert_equal(observed, expected)

    check_output_file(this_folder / 'plot_data.output.csv', test_files / 'plot_data.key.csv')


@ensure_missing(this_folder / 'plot_data2.output.png')
@ensure_missing(this_folder / 'plot_data2.output.csv')
@max_score(12.5)
@patch('requests.get', create_safe_request(max_requests=5))
def test_plot_data_four_column(request_guard_tests):
    if type(request_guard_tests) == Exception:
        assert False, 'RequestGuard must work before the rest of the assignment can be tested'

    plt.clf()
    run_python_script(
        this_folder / 'webcrawler.py', '-p',
        'https://cs111.byu.edu/Projects/project04/assets/data2.html',
        this_folder / 'plot_data2.output.png',
        this_folder / 'plot_data2.output.csv'
    )

    observed = Image(this_folder / 'plot_data2.output.png')
    expected = Image(test_files / 'plot_data2.key.png')
    assert_equal(observed, expected)

    check_output_file(this_folder / 'plot_data2.output.csv', test_files / 'plot_data2.key.csv')


def modify_images_test(images, prefix, filter):
    run_python_script(
        this_folder / 'webcrawler.py', '-i',
        'https://cs111.byu.edu/Projects/project04/assets/images.html',
        prefix, filter
    )

    for image in images:
        observed = Image(f'{prefix}{image}')
        expected = Image(test_files / f'{prefix}{image}')
        assert_equal(observed, expected)


@ensure_missing(this_folder / 's_flamingo-float.png')
@ensure_missing(this_folder / 's_landscape.png')
@ensure_missing(this_folder / 'flamingo-float.png')
@ensure_missing(this_folder / 'landscape.png')
@max_score(6.25)
@patch('requests.get', create_safe_request(max_requests=5))
def test_modify_images_sepia(request_guard_tests):
    if type(request_guard_tests) == Exception:
        assert False, 'RequestGuard must work before the rest of the assignment can be tested'
    modify_images_test(['flamingo-float.png', 'landscape.png'], 's_', '-s')


@ensure_missing(this_folder / 'g_flamingo-float.png')
@ensure_missing(this_folder / 'g_landscape.png')
@ensure_missing(this_folder / 'flamingo-float.png')
@ensure_missing(this_folder / 'landscape.png')
@max_score(6.25)
@patch('requests.get', create_safe_request(max_requests=5))
def test_modify_images_grayscale(request_guard_tests):
    if type(request_guard_tests) == Exception:
        assert False, 'RequestGuard must work before the rest of the assignment can be tested'
    modify_images_test(['flamingo-float.png', 'landscape.png'], 'g_', '-g')


@ensure_missing(this_folder / 'f_flamingo-float.png')
@ensure_missing(this_folder / 'f_landscape.png')
@ensure_missing(this_folder / 'flamingo-float.png')
@ensure_missing(this_folder / 'landscape.png')
@max_score(6.25)
@patch('requests.get', create_safe_request(max_requests=5))
def test_modify_images_vertical_flip(request_guard_tests):
    if type(request_guard_tests) == Exception:
        assert False, 'RequestGuard must work before the rest of the assignment can be tested'
    modify_images_test(['flamingo-float.png', 'landscape.png'], 'f_', '-f')


@ensure_missing(this_folder / 'm_flamingo-float.png')
@ensure_missing(this_folder / 'm_landscape.png')
@ensure_missing(this_folder / 'flamingo-float.png')
@ensure_missing(this_folder / 'landscape.png')
@max_score(6.25)
@patch('requests.get', create_safe_request(max_requests=5))
def test_modify_images_horizontal_flip(request_guard_tests):
    if type(request_guard_tests) == Exception:
        assert False, 'RequestGuard must work before the rest of the assignment can be tested'
    modify_images_test(['flamingo-float.png', 'landscape.png'], 'm_', '-m')
