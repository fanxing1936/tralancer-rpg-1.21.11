data modify storage rpg:daath t.q set value "你和谁立了约？"
scoreboard players set #v rpg_dt 0
execute store result score #v rpg_dt run scoreboard players get @a[tag=rpg.dt.me,limit=1] rpg_pact
execute store result score #r rpg_dt run random value 1..6
scoreboard players set #mod rpg_dt 8
scoreboard players operation #v1 rpg_dt = #v rpg_dt
scoreboard players operation #v1 rpg_dt += #r rpg_dt
scoreboard players operation #v2 rpg_dt = #v1 rpg_dt
scoreboard players add #v2 rpg_dt 1
scoreboard players operation #v1 rpg_dt %= #mod rpg_dt
scoreboard players operation #v2 rpg_dt %= #mod rpg_dt
execute if score #v rpg_dt matches 0 run data modify storage rpg:daath t.a0 set value "没有立约"
execute if score #v1 rpg_dt matches 0 run data modify storage rpg:daath t.a1 set value "没有立约"
execute if score #v2 rpg_dt matches 0 run data modify storage rpg:daath t.a2 set value "没有立约"
execute if score #v rpg_dt matches 1 run data modify storage rpg:daath t.a0 set value "路西法"
execute if score #v1 rpg_dt matches 1 run data modify storage rpg:daath t.a1 set value "路西法"
execute if score #v2 rpg_dt matches 1 run data modify storage rpg:daath t.a2 set value "路西法"
execute if score #v rpg_dt matches 2 run data modify storage rpg:daath t.a0 set value "利维坦"
execute if score #v1 rpg_dt matches 2 run data modify storage rpg:daath t.a1 set value "利维坦"
execute if score #v2 rpg_dt matches 2 run data modify storage rpg:daath t.a2 set value "利维坦"
execute if score #v rpg_dt matches 3 run data modify storage rpg:daath t.a0 set value "亚巴顿"
execute if score #v1 rpg_dt matches 3 run data modify storage rpg:daath t.a1 set value "亚巴顿"
execute if score #v2 rpg_dt matches 3 run data modify storage rpg:daath t.a2 set value "亚巴顿"
execute if score #v rpg_dt matches 4 run data modify storage rpg:daath t.a0 set value "别西卜"
execute if score #v1 rpg_dt matches 4 run data modify storage rpg:daath t.a1 set value "别西卜"
execute if score #v2 rpg_dt matches 4 run data modify storage rpg:daath t.a2 set value "别西卜"
execute if score #v rpg_dt matches 5 run data modify storage rpg:daath t.a0 set value "萨麦尔"
execute if score #v1 rpg_dt matches 5 run data modify storage rpg:daath t.a1 set value "萨麦尔"
execute if score #v2 rpg_dt matches 5 run data modify storage rpg:daath t.a2 set value "萨麦尔"
execute if score #v rpg_dt matches 6 run data modify storage rpg:daath t.a0 set value "贝利尔"
execute if score #v1 rpg_dt matches 6 run data modify storage rpg:daath t.a1 set value "贝利尔"
execute if score #v2 rpg_dt matches 6 run data modify storage rpg:daath t.a2 set value "贝利尔"
execute if score #v rpg_dt matches 7 run data modify storage rpg:daath t.a0 set value "玛门"
execute if score #v1 rpg_dt matches 7 run data modify storage rpg:daath t.a1 set value "玛门"
execute if score #v2 rpg_dt matches 7 run data modify storage rpg:daath t.a2 set value "玛门"
