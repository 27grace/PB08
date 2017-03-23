'''    Marks the start of comment section
-------------------------------------------------------
Name: input.py
-------------------------------------------------------
To allow for easy execution of files.
-------------------------------------------------------
'''    


def executefile():
    file_name = str(input("\nEnter file name: "))
    execfile(file_name)
    print(file_name + " is running..")

# print("\nPyBench 08\nHi Fan and Grace!\n")
# print("Tip: Use // to run files within a folder. \n")

# while True:
    # try:
        # executefile()
    # except:
        # print('\nCannot execute the file. Try again?')
        # executefile()
execfile("detectbeat_n_balance.py")