bossbar set rpg:prologue_zh name [{"translate":"rpg.prologue.N02.zh","fallback":"众天使之中有一位最明亮的，名叫路西法，就是早晨之子。神将权与力都赐给他，使他在众天使之上。","color":"#BFB8A8","italic":false}]
bossbar set rpg:prologue_en name [{"translate":"rpg.prologue.N02.en","fallback":"Among them was one brighter than all the rest, named","color":"#BFB8A8","italic":true}]
scoreboard players set #sub rpg_pr 193
scoreboard players set #subn rpg_pr 102
execute as @a[tag=rpg.pr] at @s run playsound rpg:vo.prologue.n02 voice @s ~ ~ ~ 1 1
