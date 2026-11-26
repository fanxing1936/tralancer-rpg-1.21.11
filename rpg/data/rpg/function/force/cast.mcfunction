# 按 #tree / #slot 找到槽里的技能并施放（as/at 玩家）
scoreboard players set #k rpg_fo 0
execute if score #tree rpg_fo matches 1 if score #slot rpg_fo matches 1 run scoreboard players operation #k rpg_fo = @s rpg_fs_h1
execute if score #tree rpg_fo matches 1 if score #slot rpg_fo matches 2 run scoreboard players operation #k rpg_fo = @s rpg_fs_h2
execute if score #tree rpg_fo matches 1 if score #slot rpg_fo matches 3 run scoreboard players operation #k rpg_fo = @s rpg_fs_h3
execute if score #tree rpg_fo matches 2 if score #slot rpg_fo matches 1 run scoreboard players operation #k rpg_fo = @s rpg_fs_m1
execute if score #tree rpg_fo matches 2 if score #slot rpg_fo matches 2 run scoreboard players operation #k rpg_fo = @s rpg_fs_m2
execute if score #tree rpg_fo matches 2 if score #slot rpg_fo matches 3 run scoreboard players operation #k rpg_fo = @s rpg_fs_m3
execute if score #tree rpg_fo matches 1 unless score @s rpg_force matches 1 unless score @s rpg_force matches 3 run return run function rpg:force/fail/say {m:"你没有圣力，圣徽不回应你"}
execute if score #tree rpg_fo matches 2 unless score @s rpg_force matches 2 unless score @s rpg_force matches 3 run return run function rpg:force/fail/say {m:"你没有魔力，罪印不回应你"}
execute if score #tree rpg_fo matches 1 if entity @s[tag=rpg.burnt] run return run function rpg:force/fail/say {m:"燃尽：生命力回到 30 之前，圣力不会回应你"}
execute unless score #k rpg_fo matches 1.. run return run function rpg:force/fail/say {m:"这个槽是空的：拿着它按 Shift+F 打开技能页，把技能放进槽里"}
# 达阿特：影子记住这一招（add_daath.py）
execute if score @s rpg_dt matches 1.. run scoreboard players operation @s rpg_dt_cast = #k rpg_fo
execute if score #k rpg_fo matches 1 run return run function rpg:force/sk/1/try
execute if score #k rpg_fo matches 2 run return run function rpg:force/sk/2/try
execute if score #k rpg_fo matches 3 run return run function rpg:force/sk/3/try
execute if score #k rpg_fo matches 4 run return run function rpg:force/sk/4/try
execute if score #k rpg_fo matches 5 run return run function rpg:force/sk/5/try
execute if score #k rpg_fo matches 6 run return run function rpg:force/sk/6/try
execute if score #k rpg_fo matches 7 run return run function rpg:force/sk/7/try
execute if score #k rpg_fo matches 8 run return run function rpg:force/sk/8/try
execute if score #k rpg_fo matches 9 run return run function rpg:force/sk/9/try
execute if score #k rpg_fo matches 10 run return run function rpg:force/sk/10/try
execute if score #k rpg_fo matches 11 run return run function rpg:force/sk/11/try
execute if score #k rpg_fo matches 12 run return run function rpg:force/sk/12/try
execute if score #k rpg_fo matches 13 run return run function rpg:force/sk/13/try
execute if score #k rpg_fo matches 14 run return run function rpg:force/sk/14/try
execute if score #k rpg_fo matches 15 run return run function rpg:force/sk/15/try
execute if score #k rpg_fo matches 16 run return run function rpg:force/sk/16/try
execute if score #k rpg_fo matches 17 run return run function rpg:force/sk/17/try
execute if score #k rpg_fo matches 18 run return run function rpg:force/sk/18/try
execute if score #k rpg_fo matches 19 run return run function rpg:force/sk/19/try
execute if score #k rpg_fo matches 20 run return run function rpg:force/sk/20/try
execute if score #k rpg_fo matches 21 run return run function rpg:force/sk/21/try
execute if score #k rpg_fo matches 22 run return run function rpg:force/sk/22/try
execute if score #k rpg_fo matches 23 run return run function rpg:force/sk/23/try
execute if score #k rpg_fo matches 24 run return run function rpg:force/sk/24/try
execute if score #k rpg_fo matches 25 run return run function rpg:force/sk/25/try
execute if score #k rpg_fo matches 26 run return run function rpg:force/sk/26/try
execute if score #k rpg_fo matches 31 run return run function rpg:force/sk/31/try
execute if score #k rpg_fo matches 32 run return run function rpg:force/sk/32/try
execute if score #k rpg_fo matches 33 run return run function rpg:force/sk/33/try
execute if score #k rpg_fo matches 34 run return run function rpg:force/sk/34/try
execute if score #k rpg_fo matches 35 run return run function rpg:force/sk/35/try
execute if score #k rpg_fo matches 36 run return run function rpg:force/sk/36/try
