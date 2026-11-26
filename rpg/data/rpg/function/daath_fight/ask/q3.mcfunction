data modify storage rpg:daath t.q set value "你的力从哪里来？"
scoreboard players set #v rpg_dt 0
execute store result score #v rpg_dt run scoreboard players get @a[tag=rpg.dt.me,limit=1] rpg_force
execute store result score #r rpg_dt run random value 1..2
scoreboard players set #mod rpg_dt 4
scoreboard players operation #v1 rpg_dt = #v rpg_dt
scoreboard players operation #v1 rpg_dt += #r rpg_dt
scoreboard players operation #v2 rpg_dt = #v1 rpg_dt
scoreboard players add #v2 rpg_dt 1
scoreboard players operation #v1 rpg_dt %= #mod rpg_dt
scoreboard players operation #v2 rpg_dt %= #mod rpg_dt
execute if score #v rpg_dt matches 0 run data modify storage rpg:daath t.a0 set value "没有力"
execute if score #v1 rpg_dt matches 0 run data modify storage rpg:daath t.a1 set value "没有力"
execute if score #v2 rpg_dt matches 0 run data modify storage rpg:daath t.a2 set value "没有力"
execute if score #v rpg_dt matches 1 run data modify storage rpg:daath t.a0 set value "圣力"
execute if score #v1 rpg_dt matches 1 run data modify storage rpg:daath t.a1 set value "圣力"
execute if score #v2 rpg_dt matches 1 run data modify storage rpg:daath t.a2 set value "圣力"
execute if score #v rpg_dt matches 2 run data modify storage rpg:daath t.a0 set value "魔力"
execute if score #v1 rpg_dt matches 2 run data modify storage rpg:daath t.a1 set value "魔力"
execute if score #v2 rpg_dt matches 2 run data modify storage rpg:daath t.a2 set value "魔力"
execute if score #v rpg_dt matches 3 run data modify storage rpg:daath t.a0 set value "圣力与魔力"
execute if score #v1 rpg_dt matches 3 run data modify storage rpg:daath t.a1 set value "圣力与魔力"
execute if score #v2 rpg_dt matches 3 run data modify storage rpg:daath t.a2 set value "圣力与魔力"
