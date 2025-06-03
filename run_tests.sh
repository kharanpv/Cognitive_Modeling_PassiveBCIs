#!/bin/bash

set -e

print_help() {
    echo ""
    echo "Usage: ./run_tests.sh [-type argument] [-type2 argument2] ..."
    echo ""
    echo "Available types and arguments:"
    echo "  -set <name>         Runs all tests for a specific subset of the program:"
    echo "                      all                 - All tests available for program"
    echo "                      recording_module    - Tests the Recording Module"
    echo "                      central_controller  - Tests the Central Data Controller"
    echo "                      all_handlers        - Tests all the handlers, including base class"
    echo "                      handler_class       - Tests the Handler base class"    
    echo "                      webcam_handler      - Tests the Webcam Handler"
    echo "                      screen_handler      - Tests the Screen Handler"
    echo "                      keyboard_handler    - Tests the Keyboard Handler"
    echo "                      mouse_handler       - Tests the Mouse Handler"
    echo ""
    echo "  -help               Show this help message"
    echo ""
}

if [ $# -eq 1 ] && [[ $1 == "help" || $1 == "-help" || $1 == "--help" ]]; then
    print_help
    exit 0
fi

if [ $# -lt 2 ]; then
    echo "Error: Insufficient arguments."
    print_help
    exit 1
fi

i=1
while [ $i -le $# ]; do
    TYPE=${!i}
    if [[ $TYPE != -* ]]; then
        echo "Error: Expected a flag starting with '-', got '$TYPE'"
        print_help
        exit 1
    fi
    TYPE=${TYPE#-}

    ((i++))
    OPTION=${!i}
    ((i++))

    case $TYPE in
        set)
            case $OPTION in
                all)
                    poetry run python -m pytest Tests/
                    ;;
                recording_module)
                    poetry run python -m pytest Tests/Recording_Module/
                    ;;
                central_controller)
                    poetry run python -m pytest Tests/Recording_Module/Test_Central_Data_Controller.py
                    ;;
                all_handlers)
                    poetry run python -m pytest Tests/Recording_Module/Recorders/
                    ;;
                handler_class)
                    poetry run python -m pytest Tests/Recording_Module/Recorders/Test_Handler.py
                    ;;
                webcam_handler)
                    poetry run python -m pytest Tests/Recording_Module/Recorders/Test_Webcam_Handler.py
                    ;;
                screen_handler)
                    poetry run python -m pytest Tests/Recording_Module/Recorders/Test_Screen_Handler.py
                    ;;
                keyboard_handler)
                    poetry run python -m pytest Tests/Recording_Module/Recorders/Test_Keyboard_Mouse_Handler.py::Test_Keyboard_Handler
                    ;;
                mouse_handler)
                    poetry run python -m pytest Tests/Recording_Module/Recorders/Test_Keyboard_Mouse_Handler.py::Test_Mouse_Handler
                    ;;
                *)
                    echo "Error: Unknown option '$OPTION'"
                    print_help
                    exit 1
                    ;;
            esac
            ;;
        *)
            echo "Error: Unknown type '$TYPE'"
            print_help
            exit 1
    esac
done
