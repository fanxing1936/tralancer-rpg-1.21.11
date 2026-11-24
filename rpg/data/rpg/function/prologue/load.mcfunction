scoreboard objectives add rpg_pr dummy
scoreboard objectives add rpg_pr_role dummy
scoreboard objectives add rpg_pr_id dummy
scoreboard objectives add rpg_pr_cd1 dummy
scoreboard objectives add rpg_pr_cd2 dummy
scoreboard objectives add rpg_pr_av dummy
scoreboard objectives add rpg_pr_down dummy
scoreboard objectives add rpg_pr_done dummy
scoreboard objectives add rpg_pr_lv minecraft.custom:minecraft.leave_game
scoreboard players set #ten rpg_pr 10
scoreboard players set #hund rpg_pr 100
scoreboard players set #twenty rpg_pr 20
scoreboard objectives add rpg_pr_s1 dummy
scoreboard objectives add rpg_pr_s2 dummy
execute unless score #state rpg_pr matches 0.. run scoreboard players set #state rpg_pr 0
bossbar add rpg:prologue_zh ""
bossbar add rpg:prologue_en ""
bossbar set rpg:prologue_zh color pink
bossbar set rpg:prologue_en color pink
bossbar set rpg:prologue_zh visible false
bossbar set rpg:prologue_en visible false
