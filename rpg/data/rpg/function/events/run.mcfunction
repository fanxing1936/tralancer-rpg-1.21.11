# 进行中的事件（每秒）
scoreboard players operation #left rpg_ev = #end rpg_ev
scoreboard players operation #left rpg_ev -= #now rpg_ev
scoreboard players operation #left rpg_ev /= #20 rpg_ev
execute if score #ev rpg_ev matches 1 run function rpg:events/e1/sec
execute if score #ev rpg_ev matches 2 run function rpg:events/e2/sec
execute if score #ev rpg_ev matches 3 run function rpg:events/e3/sec
execute if score #ev rpg_ev matches 4 run function rpg:events/e4/sec
execute if score #ev rpg_ev matches 5 run function rpg:events/e5/sec
execute if score #ev rpg_ev matches 6 run function rpg:merchant/ev/sec
execute if score #ev rpg_ev matches 1.. if score #left rpg_ev matches ..0 run function rpg:events/end
