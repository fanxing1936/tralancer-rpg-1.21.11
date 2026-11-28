# 对话框按钮（as/at 玩家）
scoreboard players operation #do rpg_tl = @s rpg_tl_do
scoreboard players set @s rpg_tl_do 0
scoreboard players enable @s rpg_tl_do
scoreboard players operation #t rpg_tl = @s rpg_tl_t
execute if score #do rpg_tl matches 1 run return run function rpg:town/life/gift
execute if score #do rpg_tl matches 2 run return run function rpg:town/life/ration
execute if score #do rpg_tl matches 6 run return run function rpg:town/life/buy_scroll
execute if score #do rpg_tl matches 3 run return run function rpg:town/ev/priest_info
execute if score #do rpg_tl matches 4 run return run function rpg:town/life/q/holy
execute if score #do rpg_tl matches 5 run return run function rpg:town/life/q/child
execute if score #do rpg_tl matches 11 run return run function rpg:town/life/rep
execute if score #do rpg_tl matches 12 run return run function rpg:town/life/rent
execute if score #do rpg_tl matches 13 run return run function rpg:town/life/q/letter
execute if score #do rpg_tl matches 14 run return run function rpg:town/life/q/tax
execute if score #do rpg_tl matches 15 run return run function rpg:town/life/q/wheat
execute if score #do rpg_tl matches 21 run return run function rpg:town/life/q/bard
execute if score #do rpg_tl matches 22 run return run function rpg:town/life/q/bet
execute if score #do rpg_tl matches 31 run return run function rpg:town/life/q/watch
execute if score #do rpg_tl matches 41 run return run function rpg:town/ev/start_now
execute if score #do rpg_tl matches 42 run return run function rpg:town/life/q/smith
execute if score #do rpg_tl matches 43 run return run function rpg:town/life/q/list
execute if score #do rpg_tl matches 44 run return run function rpg:town/demon/wanted_list
execute if score #do rpg_tl matches 141 run return run function rpg:town/life/q/tax_church
execute if score #do rpg_tl matches 142 run return run function rpg:town/life/q/tax_folk
