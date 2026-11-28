bossbar set rpg:prologue_zh_i4 name [{"translate":"rpg.prologue.N05.zh","fallback":"于是他们聚集在一处，希伯来话叫作哈米吉多顿。","color":"#BFB8A8","italic":false}]
bossbar set rpg:prologue_en_i4 name [{"translate":"rpg.prologue.N05.en","fallback":"And they gathered together into a place","color":"#BFB8A8","italic":true}]
scoreboard players set #sub rpg_pr_i4 82
scoreboard players set #subn rpg_pr_i4 105
execute as @a[tag=rpg.pri4] at @s run playsound rpg:vo.prologue.n05 voice @s ~ ~ ~ 1 1
