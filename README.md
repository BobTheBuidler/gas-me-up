Gas Me Up is a tool to simplify gas reimbursements for DAOs.

You will need to set the following environment variables:
 - $ETHERSCAN_TOKEN

To use this tool as a contributor:
 1. Copy the my_details_TEMPLATE.py file
 2. Rename your copy to my_details.py
 3. Specify your address(es) in the 'my_addresses' list in my_details.py
    (ENS domain names will work)
 4. Specify the address you'd like your reimbursement sent to in the 'reimbursement_address' variable
 5. Set the 'handle' variable in my_details.py to your publicly known handle
 6. If you only use these addresses for your DAO-related work, set the 'skip_confirm' veriable in my_details.py to 'True'
 7. Open a terminal and type 'brownie run gasmeup'
 8. If 'skip_confirm' is 'False', progress through the prompts to confirm each tx was made for DAO-purposes and is reimbursable
 9. Submit a PR to master

If you are using this tool to process reimbursements for contributors to your DAO, you will need the following additional environment variables:
 - $GH_PERSONAL_AUTH_TOKEN

Follow the steps here to create your auth token: https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token

To use this tool to process reimbursements for your contributors:
 1. 



