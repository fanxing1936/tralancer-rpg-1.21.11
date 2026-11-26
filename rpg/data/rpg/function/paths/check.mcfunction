# 打开新路径、更新进度、发走完的奖（as 玩家；在 rpg:sephira/tier/check 里）
scoreboard players set #new rpg_pa 0
execute if score @s rpg_sef matches 2.. unless score @s rpg_ps_32 matches 1.. run function rpg:paths/open/32
execute if score @s rpg_sef matches 3.. unless score @s rpg_ps_31 matches 1.. run function rpg:paths/open/31
execute if score @s rpg_sef matches 3.. unless score @s rpg_ps_30 matches 1.. run function rpg:paths/open/30
execute if score @s rpg_sef matches 4.. unless score @s rpg_ps_29 matches 1.. run function rpg:paths/open/29
execute if score @s rpg_sef matches 4.. unless score @s rpg_ps_28 matches 1.. run function rpg:paths/open/28
execute if score @s rpg_sef matches 4.. unless score @s rpg_ps_27 matches 1.. run function rpg:paths/open/27
execute if score @s rpg_sef matches 5.. unless score @s rpg_ps_26 matches 1.. run function rpg:paths/open/26
execute if score @s rpg_sef matches 5.. unless score @s rpg_ps_25 matches 1.. run function rpg:paths/open/25
execute if score @s rpg_sef matches 5.. unless score @s rpg_ps_24 matches 1.. run function rpg:paths/open/24
execute if score @s rpg_sef matches 6.. unless score @s rpg_ps_23 matches 1.. run function rpg:paths/open/23
execute if score @s rpg_sef matches 6.. unless score @s rpg_ps_22 matches 1.. run function rpg:paths/open/22
execute if score @s rpg_sef matches 7.. unless score @s rpg_ps_21 matches 1.. run function rpg:paths/open/21
execute if score @s rpg_sef matches 7.. unless score @s rpg_ps_20 matches 1.. run function rpg:paths/open/20
execute if score @s rpg_sef matches 7.. unless score @s rpg_ps_19 matches 1.. run function rpg:paths/open/19
execute if score @s rpg_sef matches 8.. unless score @s rpg_ps_18 matches 1.. run function rpg:paths/open/18
execute if score @s rpg_sef matches 8.. unless score @s rpg_ps_17 matches 1.. run function rpg:paths/open/17
execute if score @s rpg_sef matches 9.. unless score @s rpg_ps_16 matches 1.. run function rpg:paths/open/16
execute if score @s rpg_sef matches 9.. unless score @s rpg_ps_15 matches 1.. run function rpg:paths/open/15
execute if score @s rpg_sef matches 9.. unless score @s rpg_ps_14 matches 1.. run function rpg:paths/open/14
execute if score @s rpg_sef matches 10.. unless score @s rpg_ps_13 matches 1.. run function rpg:paths/open/13
execute if score @s rpg_sef matches 10.. unless score @s rpg_ps_12 matches 1.. run function rpg:paths/open/12
execute if score @s rpg_sef matches 10.. unless score @s rpg_ps_11 matches 1.. run function rpg:paths/open/11
execute if score #new rpg_pa matches 1.. run function rpg:paths/say_new
function rpg:paths/update
execute if score @s rpg_ps_32 matches 1 if score @s rpg_pa_32 matches 5000.. run function rpg:paths/done/32
execute if score @s rpg_ps_31 matches 1 if score @s rpg_pa_31 matches 1.. run function rpg:paths/done/31
execute if score @s rpg_ps_30 matches 1 if score @s rpg_pa_30 matches 60.. run function rpg:paths/done/30
execute if score @s rpg_ps_29 matches 1 if score @s rpg_pa_29 matches 5.. run function rpg:paths/done/29
execute if score @s rpg_ps_28 matches 1 if score @s rpg_pa_28 matches 20.. run function rpg:paths/done/28
execute if score @s rpg_ps_27 matches 1 if score @s rpg_pa_27 matches 1.. run function rpg:paths/done/27
execute if score @s rpg_ps_26 matches 1 if score @s rpg_pa_26 matches 300.. run function rpg:paths/done/26
execute if score @s rpg_ps_25 matches 1 if score @s rpg_pa_25 matches 6.. run function rpg:paths/done/25
execute if score @s rpg_ps_24 matches 1 if score @s rpg_pa_24 matches 150.. run function rpg:paths/done/24
execute if score @s rpg_ps_23 matches 1 if score @s rpg_pa_23 matches 15.. run function rpg:paths/done/23
execute if score @s rpg_ps_22 matches 1 if score @s rpg_pa_22 matches 12.. run function rpg:paths/done/22
execute if score @s rpg_ps_21 matches 1 if score @s rpg_pa_21 matches 12.. run function rpg:paths/done/21
execute if score @s rpg_ps_20 matches 1 if score @s rpg_pa_20 matches 900.. unless entity @s[tag=rpg.pl.in] run function rpg:paths/done/20
execute if score @s rpg_ps_19 matches 1 if score @s rpg_pa_19 matches 1.. run function rpg:paths/done/19
execute if score @s rpg_ps_18 matches 1 if score @s rpg_pa_18 matches 3000.. run function rpg:paths/done/18
execute if score @s rpg_ps_17 matches 1 if score @s rpg_pa_17 matches 2.. run function rpg:paths/done/17
execute if score @s rpg_ps_16 matches 1 if score @s rpg_pa_16 matches 8.. run function rpg:paths/done/16
execute if score @s rpg_ps_15 matches 1 if score @s rpg_pa_15 matches 3.. run function rpg:paths/done/15
execute if score @s rpg_ps_14 matches 1 if score @s rpg_pa_14 matches 30.. run function rpg:paths/done/14
execute if score @s rpg_ps_13 matches 1 if score @s rpg_pa_13 matches 1.. run function rpg:paths/done/13
execute if score @s rpg_ps_12 matches 1 if score @s rpg_pa_12 matches 4.. run function rpg:paths/done/12
execute if score @s rpg_ps_11 matches 1 if score @s rpg_pa_11 matches 1.. run function rpg:paths/done/11
