data modify storage rpg:daath t.q set value "你是谁？"
scoreboard players set #v rpg_dt 0
execute store result score #v rpg_dt run scoreboard players get @a[tag=rpg.dt.me,limit=1] rpg_ident
execute store result score #r rpg_dt run random value 1..5
scoreboard players set #mod rpg_dt 8
scoreboard players operation #v1 rpg_dt = #v rpg_dt
scoreboard players operation #v1 rpg_dt += #r rpg_dt
scoreboard players operation #v2 rpg_dt = #v1 rpg_dt
scoreboard players add #v2 rpg_dt 1
scoreboard players operation #v1 rpg_dt %= #mod rpg_dt
scoreboard players operation #v2 rpg_dt %= #mod rpg_dt
execute if score #v1 rpg_dt matches 0 run scoreboard players add #v1 rpg_dt 1
execute if score #v2 rpg_dt matches 0 run scoreboard players add #v2 rpg_dt 2
execute if score #v1 rpg_dt = #v rpg_dt run scoreboard players add #v1 rpg_dt 1
execute if score #v2 rpg_dt = #v rpg_dt run scoreboard players add #v2 rpg_dt 1
execute if score #v2 rpg_dt = #v1 rpg_dt run scoreboard players add #v2 rpg_dt 1
execute if score #v1 rpg_dt matches 8.. run scoreboard players set #v1 rpg_dt 1
execute if score #v2 rpg_dt matches 8.. run scoreboard players set #v2 rpg_dt 2
execute if score #v rpg_dt matches 0 run data modify storage rpg:daath t.a0 set value "没有身份"
execute if score #v1 rpg_dt matches 0 run data modify storage rpg:daath t.a1 set value "没有身份"
execute if score #v2 rpg_dt matches 0 run data modify storage rpg:daath t.a2 set value "没有身份"
execute if score #v rpg_dt matches 1 run data modify storage rpg:daath t.a0 set value "无知者"
execute if score #v1 rpg_dt matches 1 run data modify storage rpg:daath t.a1 set value "无知者"
execute if score #v2 rpg_dt matches 1 run data modify storage rpg:daath t.a2 set value "无知者"
execute if score #v rpg_dt matches 2 run data modify storage rpg:daath t.a0 set value "边缘者"
execute if score #v1 rpg_dt matches 2 run data modify storage rpg:daath t.a1 set value "边缘者"
execute if score #v2 rpg_dt matches 2 run data modify storage rpg:daath t.a2 set value "边缘者"
execute if score #v rpg_dt matches 3 run data modify storage rpg:daath t.a0 set value "神职者"
execute if score #v1 rpg_dt matches 3 run data modify storage rpg:daath t.a1 set value "神职者"
execute if score #v2 rpg_dt matches 3 run data modify storage rpg:daath t.a2 set value "神职者"
execute if score #v rpg_dt matches 4 run data modify storage rpg:daath t.a0 set value "七大罪之仆"
execute if score #v1 rpg_dt matches 4 run data modify storage rpg:daath t.a1 set value "七大罪之仆"
execute if score #v2 rpg_dt matches 4 run data modify storage rpg:daath t.a2 set value "七大罪之仆"
execute if score #v rpg_dt matches 5 run data modify storage rpg:daath t.a0 set value "圣子"
execute if score #v1 rpg_dt matches 5 run data modify storage rpg:daath t.a1 set value "圣子"
execute if score #v2 rpg_dt matches 5 run data modify storage rpg:daath t.a2 set value "圣子"
execute if score #v rpg_dt matches 6 run data modify storage rpg:daath t.a0 set value "圣灵"
execute if score #v1 rpg_dt matches 6 run data modify storage rpg:daath t.a1 set value "圣灵"
execute if score #v2 rpg_dt matches 6 run data modify storage rpg:daath t.a2 set value "圣灵"
execute if score #v rpg_dt matches 7 run data modify storage rpg:daath t.a0 set value "弥赛亚"
execute if score #v1 rpg_dt matches 7 run data modify storage rpg:daath t.a1 set value "弥赛亚"
execute if score #v2 rpg_dt matches 7 run data modify storage rpg:daath t.a2 set value "弥赛亚"
