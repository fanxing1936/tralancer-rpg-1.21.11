$execute unless data storage rpg:daath st.p$(id).w run return 0
execute at @s run summon minecraft:item_display ~ ~ ~ {Tags:["rpg.dt.ret"]}
# 区块还没载入（刚复活、刚换维度）就放不下展示实体：先留在存储里，每秒再试
execute unless entity @e[type=minecraft:item_display,tag=rpg.dt.ret,limit=1] run return 0
$data modify entity @e[type=minecraft:item_display,tag=rpg.dt.ret,limit=1] item set from storage rpg:daath st.p$(id).w.item
$data modify storage rpg:daath t.slot set from storage rpg:daath st.p$(id).w.slot
$data remove storage rpg:daath st.p$(id).w
function rpg:daath_fight/steal/put with storage rpg:daath t
kill @e[type=minecraft:item_display,tag=rpg.dt.ret]
