execute if entity @s[tag=rpg.ch1.rite] run return run function rpg:campaign/beelzebub/rite/stage4
scoreboard players remove @s rpg_ex_time 1
particle end_rod ~ ~0.9 ~ 0.9 0.55 0.9 0.05 5 force
particle soul_fire_flame ~ ~0.7 ~ 0.65 0.4 0.65 0.04 3 force
execute if score @s rpg_ex_time matches 200 run tellraw @a[distance=..14,gamemode=!spectator] ["",{"text":"[裁决尚待] ","color":"#FFF2A8","italic":false,"bold":true},{"text":"罪约尚未落笔，请选择结局。","color":"gray","italic":false}]
execute if score @s rpg_ex_time matches 200 run tellraw @a[distance=..14,gamemode=!spectator] ["",{"text":"[消灭]","color":"#FF6B5E","italic":false,"bold":true,"click_event":{"action":"run_command","command":"/trigger rpg_ex_choice set 1"}},{"text":"  ","color":"white","italic":false},{"text":"[放逐]","color":"#FFF2A8","italic":false,"bold":true,"click_event":{"action":"run_command","command":"/trigger rpg_ex_choice set 2"}},{"text":"  ","color":"white","italic":false},{"text":"[封印]","color":"#62D9E8","italic":false,"bold":true,"click_event":{"action":"run_command","command":"/trigger rpg_ex_choice set 3"}},{"text":"  ","color":"white","italic":false},{"text":"[契约]","color":"#D596F2","italic":false,"bold":true,"click_event":{"action":"run_command","command":"/trigger rpg_ex_choice set 4"}}]
execute if score @s rpg_ex_time matches ..0 run return run function rpg:inquest/outcome/banish
tag @s remove rpg.rite.anchor.active
