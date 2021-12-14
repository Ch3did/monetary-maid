```mermaid
classDiagram
class FixedDebits{
  <<Debitos Fixos do Mẽs>>
    int: id
    str: name 
    float: amount
    str: description
    date: charge_date
    

class FloatedDebits{
    <<Debitos Flutuantes do Mês>>
        int: id
        str: name 
        int: amount
        str: description
        date: charge_date
        date: due_date
        int: days_to_due
}

class Savings{
    <<History of the savings>>
    int: id
    float: big_save_amount
    float: big_save_rate
    float: investment_amount
    float: investment_rate
    float: net_amount
    float: gross_amount
    float: fixed_debits
    float: floated_debits
    date: saved_date
}
```