import automateEdapt as ae
import database as db
import automateTools

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
        ae.intervention_numbers_test_PROTOTYPE("All", driver)
    ae.intervention_numbers_test_PROTOTYPE("Mine", driver)
    ae.intervention_numbers_test_PROTOTYPE("Viewing", driver)


driver.close()