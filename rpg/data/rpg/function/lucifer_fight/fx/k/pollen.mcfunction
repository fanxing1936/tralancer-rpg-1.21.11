scoreboard players operation #f rpg_l2_v = @s rpg_l2_t
scoreboard players operation #f rpg_l2_v %= #c18 rpg_l2_v
execute if score #f rpg_l2_v matches 0 run data merge entity @s {text:{text:"",font:"rpg:lucifer_fx"}}
execute if score #f rpg_l2_v matches 3 run data merge entity @s {text:{text:"",font:"rpg:lucifer_fx"}}
execute if score #f rpg_l2_v matches 6 run data merge entity @s {text:{text:"",font:"rpg:lucifer_fx"}}
execute if score #f rpg_l2_v matches 9 run data merge entity @s {text:{text:"",font:"rpg:lucifer_fx"}}
execute if score #f rpg_l2_v matches 12 run data merge entity @s {text:{text:"",font:"rpg:lucifer_fx"}}
execute if score #f rpg_l2_v matches 15 run data merge entity @s {text:{text:"",font:"rpg:lucifer_fx"}}
