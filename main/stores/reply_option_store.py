###################
## Reply Options ##
###################
from main.utils.reply_option import ReplyOption
from main.stores.helper_function_store import make_reply_text

##########
# Common #
##########
BACK = ReplyOption("Back", "Go to previous menu")
QUIT = ReplyOption("Quit", "Exit Menu")
CANCEL = ReplyOption("Cancel", "End Session")

UNKNOWN_REPLY_MSG = ReplyOption("", "Invalid Reply\nReturning to previous menu")

#####################
# AdminConversation #
#####################
ADMIN = ReplyOption("Admin")
ADMIN_REPLY = ReplyOption("Admin Start Reply")

ENTER_MEMBER_DATA = ReplyOption("Enter", "Enter Member Information")
ENTER_DATA_FIELD = ReplyOption("Enter Data Field")
SUBMIT_MEMBER_DATA = ReplyOption("Submit", "Submit Member Data to Database")
SUBMIT_MEMBER_DATA_REPLY = ReplyOption("Submit Member Data Reply")

UPDATE_MEMBER_DATA = ReplyOption("Update", "Update Member Information")
UPDATE_MEMBER_DATA_REPLY = ReplyOption("Update Start Reply")
UPDATE_DATA_FIELD_VALUE = ReplyOption("Update Data Field Value")
UPDATE_SUBMIT = ReplyOption("Submit", "Submit Updates to Database")

DELETE_MEMBER_DATA = ReplyOption("Delete", "Delete Member Information")
DELETE_DATA_FROM_DATABASE = ReplyOption("Delete Data from Database")

#####################
# ServeConversation #
#####################
SERVE = ReplyOption("Serve")
SERVE_REPLY = ReplyOption("Serve Reply")

ROSTER = ReplyOption("Roster", "View/Swap/Replace Roster")
ROSTER_REPLY = ReplyOption("Roster Reply")

REMIND = ReplyOption("Remind", "Remind Members to update their Block Out Dates")

CREATE = ReplyOption("Create", "Create Roster")
CREATE_REPLY = ReplyOption("Create Reply")
CHECK_ROSTER_REPLY = ReplyOption("Check Roster Reply")
RECREATE_ROSTER = ReplyOption("Re-Create Roster", "Re-Create Roster")
UPLOAD_ROSTER = ReplyOption("Upload Roster", "Upload Roster to Database")

SWAP = ReplyOption("Duty Swap", "Make/Accept a Swap Duty Request")
SWAP_REPLY = ReplyOption("Swap Reply")
VIEW_MY_SWAP_OFFERS = ReplyOption("My Swap Offers", "View all offers made")
VIEW_MY_SWAP_REQUESTS = ReplyOption("My Swap Requests", "View all swap requests made")
CREATE_SWAP_REQUEST = ReplyOption("Create Swap Request", "Make a request to swap duty")
CREATE_SWAP_REQUEST_REPLY = ReplyOption("Create Swap Request Reply")
CREATE_SWAP_REQUEST_CONFIRMATION = ReplyOption("Create Swap Request Confirmation")
EDIT_SWAP_REQUEST = ReplyOption("Edit Swap Request", "Edit a swap request")
DELETE_SWAP_REQUEST = ReplyOption("Delete Swap Request", "Delete a swap request")
VIEW_MY_SWAP_REQUESTS_REPLY = ReplyOption("View My Swap Requests Reply")


REPLACE = ReplyOption("Duty Replace", "Make/Accept a Replace Duty Request")
REPLACE_REPLY = ReplyOption("Replace Reply")
CREATE_REPLACE_REQUEST = ReplyOption("Create Replace Request", "Make a Request to replace a duty")
CREATE_REPLACE_REQUEST_REPLY = ReplyOption("Create Replace Request Reply")
CREATE_REPLACE_REQUEST_CONFIRMATION = ReplyOption("Create Replace Request Confirmation")
ACCEPT_REPLACE_REQUEST = ReplyOption("Accept Replace Request", "Accept a replacement duty request")
ACCEPT_REPLACE_REQUEST_REPLY = ReplyOption("Accept Replace Request Reply")
ACCEPT_REPLACE_REQUEST_CONFIRMATION = ReplyOption("Accept Replace Request Confirmation")

BLOCK_OUT_DATES = ReplyOption("Block Out Dates", "Update/View Block Out Dates")
BLOCK_OUT_DATES_REPLY = ReplyOption("Block Out Dates Reply")
BLOCK_OUT_DATES_SUBMIT = ReplyOption("Block Out Dates Submit")

BLOCK_DATES = ReplyOption("Block Dates", "Block serving dates for next roster")
ENTER_BLOCK_OUT_DATES_MSG = make_reply_text([
    "How to Enter Block Out Dates:\n",
    "If you can't serve on the 9th and the 16th, please enter as such: 9 16" ,
    "Please leave a space after each date.",
    "Enter 0 if you are not blocking any date.\n",
    "Enter Block Out Dates: "
])

UNAUTHORISED_USE_MSG = "Unauthorised User\n" + "Going Back to previous menu"
ERROR_MSG = 'Error has occurred\n' + 'Exiting Session'
UNAUTHORISED_ACCESS_MSG = "Unauthorised Access\n\n" + "For access, please contact System Admin via /feedback\n" + "Thank You"

########################
# FeedbackConversation #
########################

FEEDBACK = ReplyOption("Feedback")
FEEDBACK_CHECK = ReplyOption("Feedback Check")
FEEDBACK_CHECK_REPLY = ReplyOption("Feedback Check Reply")

SEND = ReplyOption("Send", "Send Query to Administrator")
