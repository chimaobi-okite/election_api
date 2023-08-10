# Election_Api

This repo contains the backend codes used for the 2021/2022
Federal University of Technology, Owerri (FUTO) Society of Electrical and Electronic Engineering Students (SEEES)
elections. 

## Background and Problem Statement
Before now, the SEEES election has been administered manually using ballot papers, and results were collated via manual counting.
This process is time-consuming and very prone to rigging since there was no form of user registration and accreditation.
We witnessed situations where a single student would vote multiple times while some are struggling to cast theirs.
We also saw situations where the Independent Students' Electoral Commission would connive with the ICPC to rig elections
for particular candidates. They achieved this by secretly stamping some ballot papers and adding them to the lot before counting.

To curb this, some students built a web-based voting system. Although the system automatically counts the vote and 
displays results after voting which allowed for a faster electoral process,
it had its own shortfalls. Students were again accredited manually and used one of the provided systems 
to vote which means some students were still able to vote multiple times since there was no form of accreditation and the
ISEC could still add multiple votes from the backend since no one actually monitored this process.

## Solution and Implementation
Upon my appointment as the ISEC Chairman for the 2021/22 SEEES elections on June 20th, 2023, 
I recognized the need for reforms to ensure transparency and rectify the previously highlighted issues. 
Our refined approach encompassed the following:

1. **Voter Registration & Accreditation**:
    * The backend system was enhanced to support voter registration and accreditation.
    * This feature effectively curbed the possibility of a single user voting multiple times. Once registered, a voter could only cast their ballot once.
    * The system was designed to enable the electoral committee to upload a class list of eligible voters in a CSV format. Upon processing, this list would populate the 'Voter' table within our database.

2. Inclusion of Election Observers:

    * To ensure transparency, we integrated roles for election observers into the system. In our case, the Department's Head and Staff Adviser assumed these roles.
    * Designated as "super admins", these observers had real-time access to the election results, ensuring no foul play occurred during the tallying process.

3. Accessible Election Results:

    * Post-election, the results were made accessible to all interested parties, ensuring complete transparency in the outcome.

As a result, my department experienced one of the smoothest, most transparent, and fairest elections to date.
Many in the academic community lauded our approach, and it was universally recognized as the gold standard in the department's 
electoral history. This testament is a clear indicator of how technological advancements, 
when executed thoughtfully and responsibly, can significantly enhance traditional processes and set new benchmarks for excellence.

## Technologies Used
1. FastApi
2. Postgres database
3. SqlAlchemy
4. Alembic
5. Heroku (deployment)

## Postgres Database Schema
![election_schema_table](https://github.com/chimaobi-okite/election_api/assets/70687495/d5045fbe-5a70-4586-8c93-5d21e56598f7)

## Results
Below are sample screens from the actual election. The deployed backend has been taken down due to cost accumulation.
![1691669766639](https://github.com/chimaobi-okite/election_api/assets/70687495/ea7b4740-7302-4c92-b6cb-406236ebb0d1)
![1691669766613](https://github.com/chimaobi-okite/election_api/assets/70687495/91499c5b-5412-497b-bfae-0ad6594e34b3)
![1691669766664](https://github.com/chimaobi-okite/election_api/assets/70687495/b82ec37f-e6c1-4409-91a7-2cef6179443c)
![1691669766586](https://github.com/chimaobi-okite/election_api/assets/70687495/58e10e88-c497-4cc1-95c7-512ec56f2e0a)

## Running the FastAPI Project on Your Computer

### Prerequisites:
  * Python > 3.10 installed on your system.
  * PostgreSQL installed and running on your system.

### Steps:
1. **Clone the GitHub Repository:**

    *bash*
    ```
    git clone https://github.com/chimaobi-okite/election_api.git)
    cd election_api
    ```

2. **Set up a Virtual Environment:**

    *bash*
    ```
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```
3. **Install Dependencies:**

    *bash*
    ```
    pip install -r requirements.txt
    ```
4. **Configure PostgreSQL:**

    Start PostgreSQL and create a new database for your project.
    * Create a .env file in the project root directory
    * Update your project's database connection configuration in a .env file. Check the app.config file for the required configurations

5. **Run Alembic Migrations:**

    Before running the migrations, ensure that alembic.ini has the correct database URI.
    
    *bash*
    ```
    alembic upgrade head
    ```
6. **Start the FastAPI Application:**

    *bash*
    ```
    uvicorn app.main:app --reload
    ```

7. **Access the API:**

    Open your browser and navigate to http://localhost:8000/. 
    You should see the FastAPI default page. 
    You can also access the auto-generated docs by visiting http://localhost:8000/docs.


