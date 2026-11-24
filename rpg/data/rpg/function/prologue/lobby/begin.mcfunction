scoreboard players set #state rpg_pr 2
scoreboard players set #t rpg_pr 0
scoreboard players set #cd rpg_pr 0
scoreboard players set #taken1 rpg_pr 0
scoreboard players set #taken2 rpg_pr 0
scoreboard players set #taken3 rpg_pr 0
scoreboard players set #taken4 rpg_pr 0
bossbar set rpg:prologue_zh players @a[tag=rpg.pr]
bossbar set rpg:prologue_en players @a[tag=rpg.pr]
bossbar set rpg:prologue_zh visible true
bossbar set rpg:prologue_en visible true
function rpg:prologue/sub/u01
function rpg:prologue/music/intro
