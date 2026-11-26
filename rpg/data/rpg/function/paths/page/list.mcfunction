# 路径页（as 玩家）
function rpg:paths/update
data modify storage rpg:panel ui set value {title:{text:""},body:[],actions:[],tab:2,bw:420}
data modify storage rpg:panel ui.title set value ["",{"text":"路径","color":"#C9A646","bold":true,"italic":false},{"text":" 𝔓𝔞𝔱𝔥𝔰","color":"#8F7430","bold":false,"italic":false}]
scoreboard players operation #i rpg_pa = @s rpg_pa_32
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 5000
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b32 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p32 int 1 run scoreboard players get @s rpg_pa_32
scoreboard players operation #i rpg_pa = @s rpg_pa_31
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 1
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b31 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p31 int 1 run scoreboard players get @s rpg_pa_31
scoreboard players operation #i rpg_pa = @s rpg_pa_30
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 60
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b30 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p30 int 1 run scoreboard players get @s rpg_pa_30
scoreboard players operation #i rpg_pa = @s rpg_pa_29
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 5
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b29 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p29 int 1 run scoreboard players get @s rpg_pa_29
scoreboard players operation #i rpg_pa = @s rpg_pa_28
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 20
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b28 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p28 int 1 run scoreboard players get @s rpg_pa_28
scoreboard players operation #i rpg_pa = @s rpg_pa_27
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 1
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b27 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p27 int 1 run scoreboard players get @s rpg_pa_27
scoreboard players operation #i rpg_pa = @s rpg_pa_26
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 300
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b26 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p26 int 1 run scoreboard players get @s rpg_pa_26
scoreboard players operation #i rpg_pa = @s rpg_pa_25
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 6
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b25 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p25 int 1 run scoreboard players get @s rpg_pa_25
scoreboard players operation #i rpg_pa = @s rpg_pa_24
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 150
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b24 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p24 int 1 run scoreboard players get @s rpg_pa_24
scoreboard players operation #i rpg_pa = @s rpg_pa_23
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 15
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b23 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p23 int 1 run scoreboard players get @s rpg_pa_23
scoreboard players operation #i rpg_pa = @s rpg_pa_22
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 12
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b22 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p22 int 1 run scoreboard players get @s rpg_pa_22
scoreboard players operation #i rpg_pa = @s rpg_pa_21
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 12
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b21 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p21 int 1 run scoreboard players get @s rpg_pa_21
scoreboard players operation #i rpg_pa = @s rpg_pa_20
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 900
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b20 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p20 int 1 run scoreboard players get @s rpg_pa_20
scoreboard players operation #i rpg_pa = @s rpg_pa_19
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 1
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b19 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p19 int 1 run scoreboard players get @s rpg_pa_19
scoreboard players operation #i rpg_pa = @s rpg_pa_18
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 3000
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b18 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p18 int 1 run scoreboard players get @s rpg_pa_18
scoreboard players operation #i rpg_pa = @s rpg_pa_17
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 2
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b17 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p17 int 1 run scoreboard players get @s rpg_pa_17
scoreboard players operation #i rpg_pa = @s rpg_pa_16
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 8
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b16 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p16 int 1 run scoreboard players get @s rpg_pa_16
scoreboard players operation #i rpg_pa = @s rpg_pa_15
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 3
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b15 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p15 int 1 run scoreboard players get @s rpg_pa_15
scoreboard players operation #i rpg_pa = @s rpg_pa_14
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 30
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b14 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p14 int 1 run scoreboard players get @s rpg_pa_14
scoreboard players operation #i rpg_pa = @s rpg_pa_13
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 1
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b13 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p13 int 1 run scoreboard players get @s rpg_pa_13
scoreboard players operation #i rpg_pa = @s rpg_pa_12
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 4
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b12 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p12 int 1 run scoreboard players get @s rpg_pa_12
scoreboard players operation #i rpg_pa = @s rpg_pa_11
scoreboard players operation #i rpg_pa *= #9 rpg_pa
scoreboard players set #g rpg_pa 1
scoreboard players operation #i rpg_pa /= #g rpg_pa
execute if score #i rpg_pa matches 10.. run scoreboard players set #i rpg_pa 9
execute store result storage rpg:paths v.b11 int 1 run scoreboard players get #i rpg_pa
execute store result storage rpg:paths v.p11 int 1 run scoreboard players get @s rpg_pa_11
scoreboard players set #c rpg_pa 0
execute if score @s rpg_ps_32 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_31 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_30 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_29 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_28 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_27 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_26 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_25 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_24 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_23 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_22 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_21 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_20 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_19 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_18 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_17 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_16 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_15 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_14 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_13 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_12 matches 2.. run scoreboard players add #c rpg_pa 1
execute if score @s rpg_ps_11 matches 2.. run scoreboard players add #c rpg_pa 1
execute store result storage rpg:paths v.c int 1 run scoreboard players get #c rpg_pa
function rpg:paths/page/list_body with storage rpg:paths v
data modify storage rpg:panel ui.actions append value {"label":{"text":"‹ 生命之树","color":"#9C9A94","bold":false,"italic":false},"action":{"type":"minecraft:run_command","command":"/trigger rpg_panel set 8"}}
function rpg:panel/ui/show with storage rpg:panel ui
