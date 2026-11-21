execute store result score #t rpg_fg run data get storage rpg:forge cur.amount 1000
scoreboard players add #t rpg_fg 5
scoreboard players operation #t rpg_fg /= #10 rpg_fg
scoreboard players operation #b rpg_fg += #t rpg_fg
