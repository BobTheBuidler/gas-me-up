Gas Me Up is a tool to simplify gas reimbursements for DAOs.

You will need to set the following environment variables:
 - $ETHERSCAN_TOKEN

To use this tool as a contributor:
 0. Clone gas-me-up repo
 `git clone https://github.com/BobTheBuidler/gas-me-up`
 1. Install requirements
 `pip install -r requirements.txt`
 2. Copy the my_details_TEMPLATE.py file and rename your copy to my_details.py
 `cp my_details_TEMPLATE.py my_details.py`
 3. Edit my_details.py and fill in the variables
   - handle: TELEGRAM_HANDLE
   - skip_confirm: if False, it will prompt you to confirm which transaction are related to Yearn work. If True it will treat all transactions in that wallet as Yearn related.
   - my_addresses: an array with the address you use to do work for Yearn
   - reimbursement_address: the address where you will receive your reimbursements
 4. Copy the checkpoints sample file using your address as the filename
 `cp checkpoints/sample.csv checkpoints/0xYOURADDRESS.csv`
 5. Put the last block reimbursed into the file (The comma at the end is needed!)
 `echo "123456," > 0xYOURADDRESS.csv` 
 6. Make sure you area logged in in Github on the console
 7. Open a terminal and type 'brownie run gasmeup'
   - If skip_confirm = False, progress through the prompts to confirm each tx was made for Yearn purposes and is reimbursable.
 8. Enjoy!

If you are using this tool to process reimbursements for contributors to your DAO, you will need the following additional environment variables:
 - $GH_PERSONAL_AUTH_TOKEN

Follow the steps here to create your auth token: https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token

To use this tool to process reimbursements for your contributors:
 1. 
