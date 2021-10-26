import automateEdapt as ae
import database as db
import automateTools 
import time

user_name ="bernhard.burton"
password = "Bmoskaa1"


#Start up chrome driver
driver = automateTools.start_chrome_driver()
ae.sign_in_uat(user_name, password, driver)
ae.navigate_to_interventionsv4(driver)

#connect to UAT db
conn = db.make_EdaptUAT_conn()
school_staff = db.school_staff_query(conn)

#Prototype to compare intervention numbers and lists for all staff/school combos
cur_school_id = ""
check = False
f = open("bug_report.txt", "w")
for element in school_staff:
    if (element[0] != cur_school_id):
        cur_school_id=element[0]
        ae.change_school_to(element[0], driver)
        print("\n\nNOW UPTO SCHOOL: "+element[0]+ "\n**************************************")
        check = True
    ae.change_staff_id_to(element[1], driver)
    print("\nUPTO STAFF: " + element[1]+ "\n----------------------------------------")
    if(check):
        check = False
        ae.intervention_numbers_test_PROTOTYPE("All", driver, cur_school_id, element[1], f)
    ae.intervention_numbers_test_PROTOTYPE("Mine", driver, cur_school_id, element[1], f)
    ae.intervention_numbers_test_PROTOTYPE("Viewing", driver, cur_school_id, element[1], f)
f.close()

driver.close()