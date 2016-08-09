#!/usr/bin/env python
from __future__ import print_function

import random
from IPython.display import HTML, display
import webbrowser


def show_students(groups):
    """Display a list of student groups.

    Make student pictures display in their groups in an IPython notebook
    NB: requires that image file names are the same as student names in the
    input list.
    """
    photo_dir = './photodir/'
    # take each group list and parse student names into image file names
    # (strip space, add .jpg)
    for i in range(0, len(groups)):
        student_group = groups[i]
        list_of_image_names = []
        caption_names = ' '
        for j in range(0, len(student_group)):
            individual_names = student_group[j]
            individual_names = individual_names.replace(" ", "")
            individual_names += '.jpg'
            file_name = photo_dir + individual_names
            list_of_image_names.append(file_name)
            # we also want the student name captions to be generated
            # automatically from file names
            if j != len(student_group) - 1:
                caption_names += student_group[j] + ', '
            else:
                caption_names += student_group[j]

        # display each group member's image with their name
        preformat_html_tags = ["<figure>"]
        postformat_html_tags = ["</figure>"]
        img_fmt = "<img style='width: 200px; "
        img_fmt += "border: 1px solid black;' src='%s' />"
        image_sources = [img_fmt % str(s) for s in list_of_image_names]
        pre_captions_tag = ["<figcaption><h1>"]
        caption_mid = [caption_names]
        post_captions_tag = ["</figcaption>"]
        full_img_display_tags = preformat_html_tags + image_sources + \
            pre_captions_tag + caption_mid + \
            post_captions_tag + postformat_html_tags

        images_list = ' '.join(full_img_display_tags)
        display(HTML(images_list))


def show_students_in_browser(groups):
    """Export list of student names and potentially images to a browser.

    Make student pictures display in their groups in a local browser window
    NB: requires that image file names are the same as student names in the
    input list default browser is chrome, preferred browser can be set by
    altering the below.
    """
    browser_path = 'open -a /Applications/Google\ Chrome.app %s'
    photo_dir = './photodir/'
    outfile = open("groups.html", "w")

    # create html to go before and after code generated for student groups
    html_head = "<!DOCTYPE html><html><head>"
    style = [
        "<style>table {font-family: arial, sans-serif; ",
        "border-collapse: collapse;} ",
        "td, th {border: 1px solid #dddddd; ",
        "text-align: center; padding: 0px;} ",
        "tr:nth-child(even) {background-color: #dddddd;}",
        "</style>"
    ]
    style = "".join(style)
    html_head_end = "</head><body><table>"
    html_closing = "</table></body></html>"

    html_preamble = html_head + style + html_head_end
    # take each group list and parse student names into image file names
    # (strip space, add .jpg)
    outfile.write(html_preamble)
    for i in range(0, len(groups)):
        student_group = groups[i]
        caption_names = []
        list_of_image_names = []
        for j in range(0, len(student_group)):
            individual_names = student_group[j]
            individual_names = individual_names.replace(" ", "")
            individual_names += '.jpg'
            file_name = photo_dir + individual_names
            list_of_image_names.append(file_name)
            # we also want the student name captions to be generated
            # automatically from file names
            caption_names.append(student_group[j])

        # construct html to display each group member's image with their name
        preformat_html_tags = ["<tr>"]
        postformat_html_tags = ["</tr>"]
        linebreak = ["</tr><tr>"]
        img_td_fmt = "<td><img style='width: 200px; border: 1px solid black;' "
        img_td_fmt += "src='%s' /><td>"
        image_sources = [img_td_fmt % str(s) for s in list_of_image_names]
        caption_sources = ["<td><h1> %s </h1><td>" %
                           str(s) for s in caption_names]
        full_img_display_tags = preformat_html_tags + image_sources + \
            linebreak + caption_sources + postformat_html_tags
        images_list = ' '.join(full_img_display_tags)
        outfile.write(images_list)

    # replace the below with writing the html file and displaying it in a
    # browser window
    outfile.write(html_closing)
    outfile.close()
    brwsr = webbrowser.get(browser_path)
    brwsr.open_new('groups.html')


def name_counter(pars):
    """Return the total count of students expected from group numbers.

    Parameters consists of numbers to indicate how many groups of each size
    should be created.
    e.g. [0,8,1] will result in no students in individual groups, 8 pairs of
    students, and 1 group of 3.
    """
    total_names = 0
    i = 0
    for item in pars:
        i = i + 1
        total_names = total_names + i * pars[i - 1]
    return total_names


def get_name_list(student_file):
    """Read in student names from a file.

    Given a file that lists student names, produce Python list of student
    names.
    """
    student_names = [line.rstrip() for line in open(student_file)]

    return student_names


def shuffle_and_group_names(name_list, params):
    """Shuffle a list of names and group as desired."""
    group_container = []
    random.shuffle(name_list)
    i = 0
    num = 1
    for item in params:
        if (item != 0):
            for i in range(0, item):
                temp_group = name_list[0:num]
                group_container.append(temp_group)
                name_list.__delslice__(0, num)
        num += 1

    return group_container


def create_groups(student_file, parameters):
    """Create groups of students from a text file of student names."""
    student_names = get_name_list(student_file)
    total = name_counter(parameters)

    if total != len(student_names):
        num_students = len(student_names)
        output_msg = "There are %i students in total. " % num_students
        output_msg += "The total number of students included in groups does "
        output_msg += "not equal total number of students! Check input pars."

        print(output_msg)
        return []

    list_of_groups = shuffle_and_group_names(student_names, parameters)
    return list_of_groups


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        fname = sys.argv[1]
        namelist = get_name_list(fname)

        if len(namelist) % 2:
            group_configs = [1, int(len(namelist) / 2)]

        else:
            group_configs = [0, int(len(namelist) / 2)]

        groups = create_groups(fname, group_configs)

        print("\nGROUP PAIRS:\n")
        for group in groups:
            print("\t" + str(group))

        print("\n")

    else:
        outstr = [
            "\n              ****************************************\n",
            "              ****************************************\n",
            "              **                                    **\n",
            "              **               ERROR                **\n",
            "              **                                    **\n",
            "              ****************************************\n",
            "              ****************************************\n",
            "\nThis will not work from the command line without a file ",
            "containing a list\nof student names.\n\nEach full name should ",
            "be separated by a new line.\n\nSupply the name of the file ",
            "containing the list like so:\n\n$ python ",
            "student_group_creator.py my_name_list.txt\n"
        ]

        print("".join(outstr))
