scoreboard objectives add rpg_ev dummy
scoreboard objectives add rpg_ev_tc dummy
scoreboard objectives add rpg_bt_day dummy
scoreboard objectives add rpg_bt_total dummy
scoreboard objectives add rpg_bt_t1 dummy
scoreboard objectives add rpg_bt_t2 dummy
scoreboard objectives add rpg_bt_t3 dummy
scoreboard objectives add rpg_bt_p1 dummy
scoreboard objectives add rpg_bt_p2 dummy
scoreboard objectives add rpg_bt_p3 dummy
scoreboard objectives add rpg_bt_c1 dummy
scoreboard objectives add rpg_bt_c2 dummy
scoreboard objectives add rpg_bt_c3 dummy
scoreboard objectives add rpg_jr_do trigger
scoreboard players set #20 rpg_ev 20
scoreboard players set #8 rpg_ev 8
scoreboard players set #7 rpg_ev 7
scoreboard players set #24000 rpg_ev 24000
execute unless data storage rpg:events cur run data modify storage rpg:events cur set value {n:"",x:0,z:0}
execute unless score #ev rpg_ev matches 0.. run scoreboard players set #ev rpg_ev 0
scoreboard objectives add rpg_ev_gob dummy
scoreboard objectives add rpg_mer_day dummy
scoreboard objectives add rpg_mer_hoe dummy
