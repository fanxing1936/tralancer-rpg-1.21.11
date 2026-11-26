# 还一记影版
scoreboard players operation #e rpg_dt = @s rpg_dt_ek
scoreboard players set @s rpg_dt_ek 0
execute unless entity @s[tag=rpg.dt.echoed] run function rpg:daath_fight/echo/say
execute if score #e rpg_dt matches 1 run return run function rpg:daath_fight/skill/lance
execute if score #e rpg_dt matches 2 run return run function rpg:daath_fight/skill/blast
execute if score #e rpg_dt matches 3 run return run function rpg:daath_fight/skill/blade
execute if score #e rpg_dt matches 4 run return run function rpg:daath_fight/skill/bind
execute if score #e rpg_dt matches 5 run return run function rpg:daath_fight/skill/step
execute if score #e rpg_dt matches 6 run return run function rpg:daath_fight/skill/shell
execute if score #e rpg_dt matches 7 run return run function rpg:daath_fight/skill/puppet
execute if score #e rpg_dt matches 8 run return run function rpg:daath_fight/skill/seal
