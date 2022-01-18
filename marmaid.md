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
        float: amount
        int: instalments
        int: due_instalment
        date: init_date 
        date: end_date
        str: description
}

class Wallet{
    <<History of the savings>>
        int: id
        float: gross
        float: fixed_debits
        float: floated_debits
        float: net
        float: invest
        float: big_save
        float: month_emergency
        float: availeble
        date: date
}
```