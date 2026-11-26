data modify storage rpg:daath t.q set value "你死过几次？"
scoreboard players set #v rpg_dt 0
execute store result score #v rpg_dt run scoreboard players get @a[tag=rpg.dt.me,limit=1] rpg_dt_de
execute store result score #r rpg_dt run random value 1..4
scoreboard players operation #v1 rpg_dt = #v rpg_dt
scoreboard players operation #v1 rpg_dt += #r rpg_dt
execute store result score #r rpg_dt run random value 1..3
scoreboard players operation #v2 rpg_dt = #v rpg_dt
scoreboard players operation #v2 rpg_dt -= #r rpg_dt
execute if score #v2 rpg_dt matches ..-1 run scoreboard players operation #v2 rpg_dt = #v1 rpg_dt
execute if score #v2 rpg_dt = #v1 rpg_dt run scoreboard players add #v2 rpg_dt 2
execute store result storage rpg:daath t.a0 int 1 run scoreboard players get #v rpg_dt
execute store result storage rpg:daath t.a1 int 1 run scoreboard players get #v1 rpg_dt
execute store result storage rpg:daath t.a2 int 1 run scoreboard players get #v2 rpg_dt
