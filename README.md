# Virtuous Interview Exam

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

# Requirements

> Virtuous Data Schema, changes that require ETL have been highlighted
> <br>

<br>

![alternative text](images/virtuous_requirements.png)

## Summary

> I performed ETL of 3 spreadsheets into SQL tables & csv files that
> match the Virtuous schema <br> <br>

- Contacts: A table of contacts, with 1 or 2 constituents per row
- Gifts: Donations from individual constituents
- Contact Methods: Contact information for individual constituents

## Notebooks

> I’ve demonstrated 3 methods of performing the data migraiton <br> <br>

- [Setup](/00_Setup.ipynb) <br>
- Method 1: [SQL](01_SQL_Solution.ipynb) <br>
- Method 2: [Python / Pandas](02_Pandas_Solution.ipynb) <br>
- Method 3: [Generative AI / Chat GPT](03_Gpt_Solution.ipynb) <br>

## Result

> CSV files generated from the Python ETL process <br> <br>

- [final_contacts](data/final_contacts.csv)
- [final_gifts](data/final_gifts.csv)
- [final_contact_methods](data/final_contact_methods.csv) <br> <br> The
  intial datasets are also available in the [data folder](data/)

## My Approach

> Idea bananza!

### Call to action

> August 10th, 2:29 PM EST <br> <br>

![Email with assignment details](images/request_for_assignment.png)

### Brain STORM

> Completed: August 10th, 3:13 PM EST <br> <br>

![Rough Action Plan](images/rough_acition_plan.png)

### Take-Away

> I got a little carried away <br> <br>

Sometimes I can’t help myself! I love working with data. Finding new &
interesting ways to solve problems is something I’m naturally passionate
about <br> <br> The downside? I tend to wander a little too close to the
sun… <br> <br> While this project was simply to migrate the data to
tables compatible with the Virtuous schema, I felt a deep desire to do
more. To go above & beyond. While I pride myself on adapting to the
needs of a team, the desire to grow and change is core to who I am. And
I believe it’s a valuable asset to a great team. <br> <br> I promise to
do what’s best for the team. <br> And I also promise to always push the
boundries of what’s possible

# Final Results

``` python
import pandas as pd
```

``` python
final_contacts = pd.read_csv('data/final_contacts.csv')
final_contact_methods = pd.read_csv('data/final_contact_methods.csv')
final_gifts = pd.read_csv('data/final_gifts.csv')
```

``` python
final_contacts.fillna('')
```

<div>

|     | LegacyContactId | LegacyIndividualId | ContactName                    | ContactType  | FirstName | LastName    | SecondaryLegacyIndividualId | SecondaryFirstName | SecondaryLastName | HomePhone     | HomeEmail                    | Address1              | City         | State | PostalCode | IsPrivate | IsDeceased |
|-----|-----------------|--------------------|--------------------------------|--------------|-----------|-------------|-----------------------------|--------------------|-------------------|---------------|------------------------------|-----------------------|--------------|-------|------------|-----------|------------|
| 0   | 653377813-7     | 0                  | Karita & Kelvin Lumbers        | Household    | Karita    | Lumbers     | 1.0                         | Kelvin             | Lumbers           |               | kklumbers@yahoo.com          | 4 Bunting Parkway     | Washington   | DC    |            | True      | False      |
| 1   | 390551098-7     | 2                  | Helga Benech                   | Household    | Helga     | Benech      |                             |                    |                   |               | ebenech1@goodreads.com       | 48684 Jenifer Way     | Las Vegas    | NV    | 89130.0    | False     | False      |
| 2   | 093004505-X     | 3                  | Masha Butt Gow                 | Household    | Masha     | Butt Gow    |                             |                    |                   | 577-374-96523 |                              | 353 Schmedeman Park   | Indianapolis | IN    |            | False     | False      |
| 3   | 729707142-0     | 4                  | Cymbre Cross                   | Organization | Cymbre    | Cross       |                             |                    |                   |               |                              | 2055 Lakewood Parkway | Camden       | NJ    |            | False     | False      |
| 4   | 488464926-5     | 5                  | Hoyt Castille                  | Household    | Hoyt      | Castille    |                             |                    |                   |               | fcastille4@timesonline.co.uk | 37 8th Trail          | Grand Rapids | MI    | 49560.0    | False     | False      |
| 5   | 315297729-8     | 6                  | Benedict Oscar & Idell Mouncey | Household    | Benedict  | Oscar       | 7.0                         | Idell              | Mouncey           |               |                              | 4225 Madison Ave      | Boise        | ID    |            | False     | False      |
| 6   | 848348568-0     | 8                  | Mannie Turpin                  | Household    | Mannie    | Turpin      |                             |                    |                   | 702-844-9524  |                              |                       |              | NV    |            | False     | True       |
| 7   | 029456846-8     | 9                  | Romy Doley                     | Household    | Romy      | Doley       |                             |                    |                   |               | jdoley6@telegraph.co.uk      | 608 Old Shore Alley   | Marietta     | GA    | 30066.0    | False     | False      |
| 8   | 687119652-8     | 10                 | Ruggiero Makepeace             | Household    | Ruggiero  | Makepeace   |                             |                    |                   |               | cmakepeace7@1688.com         | 15 Sunbrook Center    | Omaha        | NE    | 68164.0    | False     | False      |
| 9   | 739131380-7     | 11                 | Rosemaria & Rogelio Dimond     | Household    | Rosemaria | Dimond      | 12.0                        | Rogelio            | Dimond            |               |                              |                       | Juneau       | AK    |            | False     | False      |
| 10  | 809975531-Y     | 13                 | Adeline Shakespeare            | Household    | Adeline   | Shakespeare |                             |                    |                   |               |                              |                       |              |       |            | False     | False      |

</div>

``` python
final_contact_methods
```

<div>

|     | LegacyContactId | Type      | Value                        |
|-----|-----------------|-----------|------------------------------|
| 0   | 093004505-X     | HomePhone | 577-374-96523                |
| 1   | 848348568-0     | HomePhone | 702-844-9524                 |
| 2   | 029456846-8     | HomeEmail | jdoley6@telegraph.co.uk      |
| 3   | 390551098-7     | HomeEmail | ebenech1@goodreads.com       |
| 4   | 488464926-5     | HomeEmail | fcastille4@timesonline.co.uk |
| 5   | 653377813-7     | HomeEmail | kklumbers@yahoo.com          |
| 6   | 687119652-8     | HomeEmail | cmakepeace7@1688.com         |
| 7   | 093004505-X     | Fax       | 818-156-7985                 |
| 8   | 739131380-7     | Fax       | 626-981-3874                 |
| 9   | 093004505-X     | HomePhone | 818-323-9865                 |
| 10  | 653377813-7     | HomePhone | 832-442-4988                 |
| 11  | 315297729-8     | HomeEmail | dmouncey9@cnn.com            |

</div>

``` python
final_gifts.fillna('')
```

<div>

|     | LegacyContactId | LegacyGiftId | GiftType              | GiftDate   | GiftAmount | Notes                     | CreditCardType | Project1Code       | Project2Code     | LegacyPledgeID |
|-----|-----------------|--------------|-----------------------|------------|------------|---------------------------|----------------|--------------------|------------------|----------------|
| 0   | 848348568-0     | 95196378     | Other                 | 2019-03-04 | 4.1500     |                           |                |                    |                  | 0              |
| 1   | 729707142-0     | 95196889     | Check                 | 2019-03-05 | 2.3648     |                           |                | ChildSponsorship   |                  | 1              |
| 2   | 687119652-8     | 95197689     | Cash                  | 2019-03-07 | 1.3100     |                           |                |                    |                  | 2              |
| 3   | 653377813-7     | 95198998     | Credit                | 2019-03-10 | 2.0400     | In honor of Mannie Turpin | AMEX           |                    |                  | 3              |
| 4   | 390551098-7     | 95198999     | Cash                  | 2019-01-10 | 5.8000     |                           |                |                    |                  | 89752384       |
| 5   | 848348568-0     | 95296677     | Other                 | 2019-03-20 | 9.2800     |                           |                | General            | ReliefFund       | 5              |
| 6   | 029456846-8     | 95298831     | Check                 | 2019-03-24 | 5.0000     | ACH check \#7687          |                |                    |                  | 6              |
| 7   | 093004505-X     | 95298845     | Check                 | 2019-04-09 | 4.8300     |                           |                |                    |                  | 7              |
| 8   | 315297729-8     | 95298997     | Check                 | 2019-04-12 | 7.0000     |                           |                | SchoolSupplies2019 |                  | 8              |
| 9   | 809975531-Y     | 9            | Credit                | 2019-08-14 | 8.4800     |                           | AMEX           |                    |                  | 9              |
| 10  | 739131380-7     | 95329966     | Credit                | 2019-04-13 | 5.8400     |                           | Visa           |                    |                  | 10             |
| 11  | 739131380-7     | 95330011     | Other                 | 2019-04-13 | 7.4500     |                           |                |                    |                  | 11             |
| 12  | 029456846-8     | 95330012     | Check                 | 2019-04-17 | 8.1300     |                           |                | Mentorship2023     |                  | 12             |
| 13  | 315297729-8     | 95330110     | Reversing Transaction | 2019-04-19 | -3.0100    |                           |                |                    |                  | 13             |
| 14  | 739131380-7     | 95330662     | Other                 | 2019-05-10 | 3.4000     |                           |                |                    |                  | 14             |
| 15  | 687119652-8     | 95419562     | Other                 | 2019-06-04 | 5.0700     |                           |                |                    |                  | 15             |
| 16  | 488464926-5     | 95422266     | Cash                  | 2019-06-05 | 5.4200     |                           |                | GeneralFund        |                  | 16             |
| 17  | 848348568-0     | 95485564     | Other                 | 2019-06-10 | 6.8000     |                           |                |                    |                  | 57398862       |
| 18  | 390551098-7     | 95496635     | Other                 | 2019-06-11 | 6.7800     |                           |                |                    |                  | 18             |
| 19  | 729707142-0     | 95497782     | Other                 | 2019-06-20 | 5.2700     |                           |                |                    |                  | 19             |
| 20  | 315297729-8     | 20           | Check                 | 2019-06-20 | 5.5900     |                           |                |                    |                  | 65139856       |
| 21  | 390551098-7     | 95763575     | Credit                | 2019-07-01 | 4.2100     |                           | Mastercard     |                    |                  | 21             |
| 22  | 488464926-5     | 95798342     | Cash                  | 2019-07-18 | 9.2800     |                           |                |                    |                  | 22             |
| 23  | 848348568-0     | 95798343     | Other                 | 2019-07-01 | 2.7400     |                           |                |                    |                  | 23             |
| 24  | 029456846-8     | 95801563     | Other                 | 2019-08-01 | 9.0000     |                           |                |                    |                  | 24             |
| 25  | 729707142-0     | 95801564     | Cash                  | 2019-08-03 | 1.8800     |                           |                |                    |                  | 25             |
| 26  | 687119652-8     | 95835492     | Reversing Transaction | 2019-08-12 | -6.7600    |                           |                |                    |                  | 26             |
| 27  | 809975531-Y     | 27           | Credit                | 2019-08-14 | 7.5800     |                           | Mastercard     | Color run          | ChildSponsorship | 27             |
| 28  | 653377813-7     | 28           | Cash                  | 2019-08-26 | 5.4900     |                           |                |                    |                  | 28             |
| 29  | 739131380-7     | 96638462     | Other                 | 2019-09-01 | 8.9300     |                           |                | ReliefFund         |                  | 29             |
| 30  | 093004505-X     | 96638468     | Credit                | 2019-09-06 | 2.6200     |                           | Discover       |                    |                  | 30             |

</div>
