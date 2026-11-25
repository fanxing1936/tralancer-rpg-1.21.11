# 揭开一件
function rpg:vault/roll
data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{translation:[0.000f,0.000f,1.600f],scale:[0.560f,0.560f,0.560f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}
playsound minecraft:block.vault.eject_item block @a[distance=..16] ~ ~ ~ 0.9 1.1
execute if score #q rpg_vt matches 1 positioned ^ ^ ^1.60 run function rpg:vault/pop_1
execute if score #q rpg_vt matches 2 positioned ^ ^ ^1.60 run function rpg:vault/pop_2
execute if score #q rpg_vt matches 3 positioned ^ ^ ^1.60 run function rpg:vault/pop_3
execute if score #q rpg_vt matches 4 positioned ^ ^ ^1.60 run function rpg:vault/pop_4
