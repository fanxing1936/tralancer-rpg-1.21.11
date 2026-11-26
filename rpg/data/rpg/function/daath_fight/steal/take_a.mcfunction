# 夺一件盔甲：有哪件抽哪件
scoreboard players set #r rpg_dt 0
execute store result score #o rpg_dt run random value 0..3
scoreboard players set #f rpg_dt 0
execute if score #o rpg_dt matches 0 if score #f rpg_dt matches 0 if items entity @a[tag=rpg.dt.me,limit=1] armor.chest * run function rpg:daath_fight/steal/take_chest
execute if score #o rpg_dt matches 0 if score #f rpg_dt matches 0 if items entity @a[tag=rpg.dt.me,limit=1] armor.head * run function rpg:daath_fight/steal/take_head
execute if score #o rpg_dt matches 0 if score #f rpg_dt matches 0 if items entity @a[tag=rpg.dt.me,limit=1] armor.legs * run function rpg:daath_fight/steal/take_legs
execute if score #o rpg_dt matches 0 if score #f rpg_dt matches 0 if items entity @a[tag=rpg.dt.me,limit=1] armor.feet * run function rpg:daath_fight/steal/take_feet
execute if score #o rpg_dt matches 1 if score #f rpg_dt matches 0 if items entity @a[tag=rpg.dt.me,limit=1] armor.head * run function rpg:daath_fight/steal/take_head
execute if score #o rpg_dt matches 1 if score #f rpg_dt matches 0 if items entity @a[tag=rpg.dt.me,limit=1] armor.legs * run function rpg:daath_fight/steal/take_legs
execute if score #o rpg_dt matches 1 if score #f rpg_dt matches 0 if items entity @a[tag=rpg.dt.me,limit=1] armor.feet * run function rpg:daath_fight/steal/take_feet
execute if score #o rpg_dt matches 1 if score #f rpg_dt matches 0 if items entity @a[tag=rpg.dt.me,limit=1] armor.chest * run function rpg:daath_fight/steal/take_chest
execute if score #o rpg_dt matches 2 if score #f rpg_dt matches 0 if items entity @a[tag=rpg.dt.me,limit=1] armor.legs * run function rpg:daath_fight/steal/take_legs
execute if score #o rpg_dt matches 2 if score #f rpg_dt matches 0 if items entity @a[tag=rpg.dt.me,limit=1] armor.feet * run function rpg:daath_fight/steal/take_feet
execute if score #o rpg_dt matches 2 if score #f rpg_dt matches 0 if items entity @a[tag=rpg.dt.me,limit=1] armor.chest * run function rpg:daath_fight/steal/take_chest
execute if score #o rpg_dt matches 2 if score #f rpg_dt matches 0 if items entity @a[tag=rpg.dt.me,limit=1] armor.head * run function rpg:daath_fight/steal/take_head
execute if score #o rpg_dt matches 3 if score #f rpg_dt matches 0 if items entity @a[tag=rpg.dt.me,limit=1] armor.feet * run function rpg:daath_fight/steal/take_feet
execute if score #o rpg_dt matches 3 if score #f rpg_dt matches 0 if items entity @a[tag=rpg.dt.me,limit=1] armor.chest * run function rpg:daath_fight/steal/take_chest
execute if score #o rpg_dt matches 3 if score #f rpg_dt matches 0 if items entity @a[tag=rpg.dt.me,limit=1] armor.head * run function rpg:daath_fight/steal/take_head
execute if score #o rpg_dt matches 3 if score #f rpg_dt matches 0 if items entity @a[tag=rpg.dt.me,limit=1] armor.legs * run function rpg:daath_fight/steal/take_legs
