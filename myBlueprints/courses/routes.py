from flask import flash,Blueprint,render_template,redirect,url_for,session,request,jsonify


courses_pg = Blueprint(
                        "courses_pg",
                        __name__,
                        template_folder="templates",
                        static_folder="coursesStatics"
                    )

@courses_pg.route("/afterLoginCourses")
def mainCoursesPage():
    return render_template('coursesList.html')

# @courses_pg.route("/pythonCourses")
# def pythonCoursePage():
#     return render_template('pythonCourse.html')

@courses_pg.route('/course/python')
def course_python():
    chapters = [
        {"id": 1, "title": "Introduction to Python"},
        {"id": 2, "title": "Python Installation Guide"},
        {"id": 3, "title": "Python set path in windows"},
        {"id": 4, "title": "Variables in python"},
        {"id": 5, "title": "Data types in python"},
        {"id": 6, "title": "Operators in python"},
        {"id": 7, "title": "Conditional statments in python"},
        {"id": 8, "title": "User input in python"},
        {"id": 9, "title": "Swap variables in python"},
        {"id": 10, "title": "List in python"},
        {"id": 11, "title": "Tuple and set in python"},
        {"id": 12, "title": "Dictionary in python"}
    ]
    return render_template('pythonCourse.html', chapters=chapters, course="Python")

# Serve the Java course page
@courses_pg.route('/course/java')
def course_java():
    chapters = [
        {"id": 1, "title": "Introduction to Java"},
        {"id": 2, "title": "JVM (Java virtual machine)"},
        {"id": 3, "title": "Comments in java"},
        {"id": 4, "title": "Data types in java"},
        {"id": 5, "title": "Operators in java"},
        {"id": 6, "title": "Controll statments in java"},
        {"id": 7, "title": "Input & Output in java"},
        {"id": 8, "title": "Arrays in java)"},
        {"id": 9, "title": "Multi dimensional array in java"},
        {"id": 10, "title": "Strings in java"},
        {"id": 11, "title": "Classes and objects in java"},
        {"id": 12, "title": "Methods in java"}
    ]
    return render_template('javaCourse.html', chapters=chapters, course="Java")

# Serve the C course page
@courses_pg.route('/course/c')
def course_c():
    chapters = [
        {"id": 1, "title": "Introduction to C"},
        {"id": 2, "title": "Operators in C"},
        {"id": 3, "title": "Conditional statments in C"},
        {"id": 4, "title": "Loops to C"},
        {"id": 5, "title": "Functions and recursion in C"},
        {"id": 6, "title": "Pointers in C"},
        {"id": 7, "title": "Arrays to C"},
        {"id": 8, "title": "Strings in C"},
        {"id": 9, "title": "Structures in C"},
        {"id": 10, "title": "Files in C"}
    ]
    return render_template('cCourse.html', chapters=chapters, course="C")




# Return chapter content as JSON
@courses_pg.route('/course_content/<course>/<int:chapter_id>')
def load_content(course, chapter_id):
    content_data = {
        'Python': {
            1: {"title": "Introduction to Python",
                "content": render_template("forPython/introToPython.html"), 
                "video_id": "hEgO047GxaQ?si=lFhfwL16g2TvQcIo"
                },
            2: {"title": "Python Installation Guide", 
                "content": render_template('forPython/python_installation.html'), 
                "video_id": "CScxy0294SE?si=bmpcGSNHA6BDPiS3"
                },
            3: {"title": "Python set path in windows", 
                "content": render_template("forPython/python_set_path_in_windows.html"), 
                "video_id": "4V14G5_CNGg?si=gDGw6S42TOEqz-sl"
                },
            4: {"title": "Variables in python", 
                "content": render_template('forPython/variables_in_python.html'),        "video_id": "TqPzwenhMj0?si=qetSlmqv4ew88zp5"
                },
            5: {"title": "Data types in python", 
                "content": render_template('forPython/datatypes_in_python.html'),
                "video_id": "gCCVsvgR2KU?si=_QnVWo9wdXGA-Rus"
                },
            6: {"title": "Operators in python", 
                "content": render_template('forPython/operators_in_python.html'),
                "video_id": "v5MR5JnKcZI?si=HIZkmTBJUqKmI88A"
                },
            7: {"title": "Conditional statments in python", 
                "content": render_template('forPython/conditional_flow_statments_python.html'), 
                "video_id": "PqFKRqpHrjw?si=6aBIBgZaOaGYayM1"
                },
            8: {"title": "User input in python",
                "content": render_template('forPython/user_input_in_python.html'), 
                "video_id": "4OX49nLNPEE?si=IyNOnuQGKSJ5zlny"
                },
            9: {"title": "Swap variables in python", 
                "content": render_template('forPython/swap_variables_in_python.html'), 
                "video_id": "3dpJrMtxYeo?si=sNfRAd8zNp6neb8t"
                },
            10: {"title": "List in python",
                 "content": render_template('forPython/list_in_python.html'),
                 "video_id": "Eaz5e6M8tL4?si=rJKnpYcdIoSxs2vf"
                 },
            11: {"title": "Tuple and set in python",
                 "content": render_template('forPython/python_installation.html'), 
                 "video_id": "Mf7eFtbVxFM?si=PuqU50dw9R5wokJd"
                 },
            12: {"title": "Dictionary in python", 
                 "content": render_template('forPython/dictionary_in_python.html'), 
                 "video_id": "2IsF7DEtVjg?si=tLGtNxOIAB4I309E"
                 }
        },
        'Java': {
            1: {"title": "Introduction to Java", 
                "content": render_template("forJava/intro_to_java.html"), 
                "video_id": "AfBCK1PaXgU?si=54CRNQE0vxUgbbj7"
                },
            2: {"title": "JVM (Java virtual machine)",
                "content": render_template("forJava/jvm.html"),
                "video_id": "VY0u8LQZQ_U?si=RTJUL9KBE2BFp2EA"
                },
            3: {"title": "Comments in java", 
                "content": render_template("forJava/comments_in_java.html"), 
                "video_id": "kgzkkfp6Sb4?si=7h2jR12qpTL1kHnp"
                },
            4: {"title": "Data types in java", 
                "content": render_template("forJava/datatypes_in_java.html"), 
                "video_id": "tiadbMfdVQg?si=nONxDGIiRn4t5lCU"
                },
            5: {"title": "Operators in java",
                "content": render_template("forJava/operators_in_java.html"),
                "video_id": "McVd0Hbymko?si=EPqxSj138R9c_L_J"
                },
            6: {"title": "Controll statments in java", 
                "content": render_template("forJava/control_statements_in_java.html"),
                "video_id": "MMogWTFq2Uo?si=P0e7c-G9ckrypJlX"
                },
            7: {"title": "Input & Output in java", 
                "content": render_template("forJava/input_and_ouput_in_java.html"),
                "video_id": "YrtOKZLK3l0?si=_Z6EEINZMcPOg7xJ"
                },
            8: {"title": "Arrays in java",
                "content": render_template("forJava/arrays_in_java.html"), 
                "video_id": "-UMhk7WZHvU?si=60OfbnqwWLtmzxtz"
                },
            9: {"title": "Multi dimensional arrays in java", 
                "content": render_template("forJava/multidimesional_array_in_java.html"), 
                "video_id": "6H37wwMHRBY?si=tPVz4xu1wzKJfwXz"
                },
            10: {"title": "Strings in java", 
                "content": render_template("forJava/strings_in_java.html"), 
                "video_id": "J2iNGatyVuQ?si=35K-iADXgis8xXyP"
                },
            11: {"title": "Classes & Objects in java",
                "content": render_template("forJava/classes_objects_in_java.html"), 
                "video_id": "q9PicUhFHHQ?si=bAaU2Lpge1Ldzn5E"
                },
            12: {"title": "Methods in java", 
                "content": render_template("forJava/methods_in_java.html"),
                "video_id": "xjGiimRGlAw?si=vMsluJK5C9bBORi3"
                }
        },
        'C': {
            1: {"title": "Introduction to C",
                "content": render_template("forC/intro_to_c.html"), 
                "video_id": "J-eV_1Dje9U?si=H9NhcFZQyMmA_c3X"
                },
            2: {"title": "Operators in c", 
                "content": render_template("forC/operators_in_c.html"), 
                "video_id": "tTpPUq7dtZo?si=KOTzYBkSYARAAPAe"
                },
            3: {"title": "Conditional Statments in C", 
                "content": render_template("forC/conditional_in_c.html"), 
                "video_id": "YiPoFeWrSYY?si=_Bu8vG7oFTomH1n7"
                },
            4: {"title": "Loops in c", 
                "content": render_template("forC/loops_in_c.html"), 
                "video_id": "YiPoFeWrSYY?si=sVxhM11Od7-Ljvdh"
                },
            5: {"title": "Functions & recursions in c", 
                "content": render_template("forC/functions_recurrsion_in_c.html"), 
                "video_id": "K4MA1Hkwj0s?si=MvlJC3bQ6DST-IuL"
                },
            6: {"title": "Pointers in c", 
                "content": render_template("forC/pointers_in_c.html"), 
                "video_id": "lAFwEkd1P6w?si=A2vV4BkSxiN7yLhw"
                },
            7: {"title": "Arrays in c", 
                "content": render_template("forC/arrays_in_c.html"), 
                "video_id": "Mubmm7rqjK4?si=0u5YEYRCbw7yTXRY"
                },
            8: {"title": "Strings in c", 
                "content": render_template("forC/strings_in_c.html"), 
                "video_id": "m4wVJuaQu_4?si=XuhaPHU2mMX3-vAW"
                },
            9: {"title": "Structures in c", 
                "content": render_template("forC/strucutres_in_c.html"), 
                "video_id": "c1d987iBBJ0?si=BIf_DlsfMvWiqDwp"
                },
            10: {"title": "Files in c", 
                "content": render_template("forC/files_in_c.html"), 
                "video_id": "ltGqiqZJ3aI?si=7LffnY8nhmD3SHLz"
                }
        }
    }
    
    course_content = content_data.get(course, {}).get(chapter_id, {})
    return jsonify(course_content)
