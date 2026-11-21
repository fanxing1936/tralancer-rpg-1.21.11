scoreboard players set @s rpg_fg_op 2
execute store result score #q rpg_fg run data get storage rpg:forge e.q
execute if data storage rpg:forge e.pq store result score #pq rpg_fg run data get storage rpg:forge e.pq
execute unless data storage rpg:forge e.pq run function rpg:forge/op/wash/roll
data modify storage rpg:forge d.as set value ""
execute if score #q rpg_fg matches 0.. run data modify storage rpg:forge d.as set value "+"
execute store result storage rpg:forge d.a int 1 run scoreboard players get #q rpg_fg
execute if score #q rpg_fg matches -100..-6 run data modify storage rpg:forge d.an set value "残次"
execute if score #q rpg_fg matches -5..5 run data modify storage rpg:forge d.an set value "普通"
execute if score #q rpg_fg matches 6..10 run data modify storage rpg:forge d.an set value "精良"
execute if score #q rpg_fg matches 11..15 run data modify storage rpg:forge d.an set value "完美"
data modify storage rpg:forge d.bs set value ""
execute if score #pq rpg_fg matches 0.. run data modify storage rpg:forge d.bs set value "+"
execute store result storage rpg:forge d.b int 1 run scoreboard players get #pq rpg_fg
execute if score #pq rpg_fg matches -100..-6 run data modify storage rpg:forge d.bn set value "残次"
execute if score #pq rpg_fg matches -5..5 run data modify storage rpg:forge d.bn set value "普通"
execute if score #pq rpg_fg matches 6..10 run data modify storage rpg:forge d.bn set value "精良"
execute if score #pq rpg_fg matches 11..15 run data modify storage rpg:forge d.bn set value "完美"
function rpg:forge/op/wash/show with storage rpg:forge d
