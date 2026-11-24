scoreboard players set @s rpg_ident 1
execute store result score #u rpg_ob run random value 0..2
execute if score #u rpg_ob matches 0 if score @s rpg_ident matches 1 unless data storage rpg:onboard taken.son run function rpg:onboard/ident/take_son
execute if score #u rpg_ob matches 0 if score @s rpg_ident matches 1 unless data storage rpg:onboard taken.spirit run function rpg:onboard/ident/take_spirit
execute if score #u rpg_ob matches 0 if score @s rpg_ident matches 1 unless data storage rpg:onboard taken.messiah run function rpg:onboard/ident/take_messiah
execute if score #u rpg_ob matches 1 if score @s rpg_ident matches 1 unless data storage rpg:onboard taken.spirit run function rpg:onboard/ident/take_spirit
execute if score #u rpg_ob matches 1 if score @s rpg_ident matches 1 unless data storage rpg:onboard taken.messiah run function rpg:onboard/ident/take_messiah
execute if score #u rpg_ob matches 1 if score @s rpg_ident matches 1 unless data storage rpg:onboard taken.son run function rpg:onboard/ident/take_son
execute if score #u rpg_ob matches 2 if score @s rpg_ident matches 1 unless data storage rpg:onboard taken.messiah run function rpg:onboard/ident/take_messiah
execute if score #u rpg_ob matches 2 if score @s rpg_ident matches 1 unless data storage rpg:onboard taken.son run function rpg:onboard/ident/take_son
execute if score #u rpg_ob matches 2 if score @s rpg_ident matches 1 unless data storage rpg:onboard taken.spirit run function rpg:onboard/ident/take_spirit
