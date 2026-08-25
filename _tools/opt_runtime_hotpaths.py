# -*- coding: utf-8 -*-
"""Optimize real tick hot paths after all content generators have run."""

import io
import os
import re
import sys

DP = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "../rpg")
FUNC = os.path.join(DP, "data/rpg/function")


def path(rel):
    return os.path.join(FUNC, rel.replace("/", os.sep))


def read(rel):
    return io.open(path(rel), encoding="utf-8").read()


def write(rel, text):
    p = path(rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text.rstrip() + "\n")


def add_objective(name):
    rel = "command/soreboard.mcfunction"
    text = read(rel)
    line = "scoreboard objectives add %s dummy" % name
    if line not in text:
        write(rel, text.rstrip() + "\n" + line)


def localise(rel, prefix):
    out = []
    for line in read(rel).splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        if not line.startswith(prefix):
            raise AssertionError("%s: unexpected line: %s" % (rel, line))
        line = line[len(prefix):]
        if line.startswith("run "):
            line = line[4:]
        elif not line.startswith("execute "):
            line = "execute " + line
        out.append(line)
    return out


def cap_boss_particle(line):
    for old, new in {
        " 1 1000": " 1 96",
        " 0 300 force": " 0 72 normal",
        " 1 100": " 1 24",
        " 0.1 50": " 0.1 16",
    }.items():
        line = line.replace(old, new)
    return line


def optimize_warden():
    g0 = localise("entities/warden/warden/g0.mcfunction",
                  "execute as @e[tag=devil] at @s ")
    g1 = localise("entities/warden/warden/g1.mcfunction",
                  "execute as @e[tag=devil] at @s ")
    g2 = [cap_boss_particle(x) for x in localise(
        "entities/warden/warden/g2.mcfunction",
        "execute as @e[tag=devil,tag=boss] at @s ")]
    g3 = localise("entities/warden/warden/g3.mcfunction",
                  "execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s ")
    g4 = [cap_boss_particle(x) for x in localise(
        "entities/warden/warden/g4.mcfunction",
        "execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s ")]

    write("entities/warden/phase1_entity.mcfunction", "\n".join(
        ["# 单次实体绑定完成一阶段常驻逻辑。"] + g0 + [
            "execute if score @s devil matches 200.. run scoreboard players set @s devil 0",
            "scoreboard players add @s devil 1",
            "execute if entity @s[tag=rpg.boss.minion] run scoreboard players add @s rpg_boss_fx 1",
            "execute if entity @s[tag=rpg.boss.minion,scores={rpg_boss_fx=1200..}] run return run kill @s",
        ] + g1 + [
            "execute if entity @s[tag=boss] run function rpg:entities/warden/phase1_boss",
        ]))
    write("entities/warden/phase1_minion.mcfunction", '''
# 只在真正掷中召唤技时统计；附近最多保留六只一阶段侍从。
scoreboard players set #boss_minions rpg_boss_fx 0
execute as @e[tag=devil,tag=!boss,distance=..24] run scoreboard players add #boss_minions rpg_boss_fx 1
execute if score #boss_minions rpg_boss_fx matches ..5 at @a[distance=..20,limit=1,sort=random] run playsound minecraft:entity.ghast.hurt player @a[distance=..15]
execute if score #boss_minions rpg_boss_fx matches ..5 at @a[distance=..20,limit=1,sort=random] run summon vindicator ~ ~ ~ {Johnny:1,Health:50,Silent:1b,Tags:["devil","rpg.boss.minion"],active_effects:[{id:speed,duration:-1,amplifier:1,show_particles:0b}],attributes:[{id:attack_knockback,base:2f},{id:"max_health",base:100f}]}
''')
    write("entities/warden/phase1_boss.mcfunction", "\n".join([
        "execute if score @s devil matches 150 store result score @s random run random value 1..3",
        "execute if score @s random matches 1 if score @s devil matches 150 run function rpg:entities/warden/phase1_minion",
        "execute if score @s random matches 2 if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run playsound minecraft:entity.ghast.death player @a[distance=..15]",
        "execute if score @s random matches 2 if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run effect give @s slowness 3 255 true",
        "execute if score @s random matches 2 if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run effect give @s glowing 3 255 true",
        "execute if score @s random matches 2 if score @s devil matches 150 at @a[distance=..20,limit=1,sort=random] run damage @s 10 minecraft:wither",
        "scoreboard players reset @s random",
    ] + g2))
    write("entities/warden/phase1.mcfunction", '''
execute as @e[tag=devil] at @s run function rpg:entities/warden/phase1_entity
# 旧实现遍历所有实体的 attacker；实际只需揭露攻击恶魔的人。
execute as @e[tag=devil] on attacker at @s run function rpg:entities/warden/reveal_attacker
''')
    write("entities/warden/reveal_attacker.mcfunction", '''
effect clear @s minecraft:invisibility
effect give @s minecraft:glowing 1 1 true
''')

    g3 = [x.replace('CustomName:[{"text":"devil_attack"}],Invulnerable:1b',
                    'CustomName:[{"text":"devil_attack"}],Invulnerable:1b,Tags:["rpg.boss.slash","rpg.boss.slash.new"]')
          for x in g3]
    g4 = [x.replace('Tags:["devil2","tick","rpg.pseudo_boom.minion_new"]',
                    'Tags:["devil2","tick","rpg.pseudo_boom.minion_new","rpg.boss.minion2"]')
          for x in g4]
    g3 = [x.replace("@e[name=devil_attack,type=armor_stand]",
                    "@e[type=minecraft:armor_stand,tag=rpg.boss.slash.new]")
          for x in g3]
    g3.append("tag @e[type=minecraft:armor_stand,tag=rpg.boss.slash.new] remove rpg.boss.slash.new")
    write("entities/warden/phase2_boss.mcfunction", "\n".join([
        "execute if score @s devil matches 400.. run scoreboard players set @s devil 0",
        "scoreboard players add @s devil 1",
    ] + g3 + g4))
    write("entities/warden/phase2_entity.mcfunction", '''
execute if entity @s[tag=rpg.boss.minion2] run scoreboard players add @s rpg_boss_fx 1
execute if entity @s[tag=rpg.boss.minion2,scores={rpg_boss_fx=1200..}] run return run kill @s
execute if entity @s[tag=rpg.boss.minion2] unless entity @e[type=minecraft:vindicator,tag=devil2,tag=boss,limit=1] run return run kill @s
execute if entity @e[type=minecraft:area_effect_cloud,limit=1,distance=..2] run effect give @s minecraft:instant_damage 1 1 true
execute if entity @e[type=minecraft:area_effect_cloud,limit=1,distance=..2] run particle trial_spawner_detection_ominous ~0.2 ~1.2 ~0.2 -0.4 -0.4 -0.4 0 10
execute if entity @s[tag=boss] run function rpg:entities/warden/phase2_boss
''')
    write("entities/warden/phase2.mcfunction", '''
execute as @a[scores={devil_hurt=0..}] at @s on attacker if entity @s[tag=devil2] run particle large_smoke ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 10
execute as @a[scores={devil_hurt=0..}] at @s on attacker if entity @s[tag=devil2] run particle sweep_attack ~0.5 ~1.5 ~0.5 -1 -1 -1 0.1 10
execute as @a[scores={devil_hurt=0..}] at @s on attacker if entity @s[tag=devil2,tag=boss] run effect give @e[limit=1] minecraft:wither 5 3 true
scoreboard players reset * devil_hurt
execute as @e[type=minecraft:vindicator,tag=devil2] at @s run function rpg:entities/warden/phase2_entity
''')
    write("entities/warden/slash_entity.mcfunction", '''
particle minecraft:sweep_attack ~0.5 ~1.2 ~0.5 -1 -1 -1 0 6 normal
particle large_smoke ~0.5 ~1.2 ~0.5 -1 -1 -1 0.2 6 normal
execute anchored feet run tp @s ^ ^ ^1
execute anchored feet run damage @e[limit=1,sort=nearest,distance=0.1..3,tag=ashes] 20 minecraft:outside_border
scoreboard players add @s rpg_boss_fx 1
execute if score @s rpg_boss_fx matches 20.. run kill @s
execute unless entity @e[type=minecraft:vindicator,distance=..50,tag=devil2] run kill @s
''')
    write("entities/warden/slashes.mcfunction",
          "execute as @e[type=minecraft:armor_stand,tag=rpg.boss.slash] at @s run function rpg:entities/warden/slash_entity")
    optimize_bossbars()
    add_objective("rpg_boss_fx")


def optimize_bossbars():
    ids = ("devil", "devil2", "devil3", "devil4")
    write("entities/warden/bossbar_entity.mcfunction", "\n".join([
        "execute unless score @s rpg_boss_slot = @s rpg_boss_slot run function rpg:entities/warden/bossbar_allocate",
        "execute if score @s rpg_boss_slot matches 0 run function rpg:entities/warden/bossbar_allocate",
    ] + ["execute if score @s rpg_boss_slot matches %d run return run function rpg:entities/warden/bossbar_show%d" % (n, n)
         for n in range(1, 5)]))
    write("entities/warden/bossbar_tick.mcfunction", "\n".join([
        "scoreboard players add #boss_slot%d rpg_boss_slot 0" % n for n in range(1, 5)
    ] + [
        "execute as @e[type=minecraft:evoker,tag=boss] at @s run function rpg:entities/warden/bossbar_entity",
        "execute as @e[type=minecraft:vindicator,tag=devil2,tag=boss] at @s run function rpg:entities/warden/bossbar_entity",
    ]))
    write("entities/warden/bossbar_clock.mcfunction", '''
scoreboard players add #boss_ui rpg_boss_slot 1
execute if score #boss_ui rpg_boss_slot matches 2.. run function rpg:entities/warden/bossbar_tick
execute if score #boss_ui rpg_boss_slot matches 2.. run scoreboard players set #boss_ui rpg_boss_slot 0
''')
    write("entities/warden/bossbar_probe_tick.mcfunction",
          "execute as @e[type=minecraft:marker,tag=rpg.bossbar.probe] run function rpg:entities/warden/bossbar_probe")
    probe = ["execute on vehicle run return 0"]
    for n, bid in enumerate(ids, 1):
        probe.extend([
            "execute if score @s rpg_boss_slot matches %d run scoreboard players set #boss_slot%d rpg_boss_slot 0" % (n, n),
            "execute if score @s rpg_boss_slot matches %d run bossbar set minecraft:%s players @a[tag=rpg.bossbar.none]" % (n, bid),
        ])
    probe.append("kill @s")
    write("entities/warden/bossbar_probe.mcfunction", "\n".join(probe))
    write("entities/warden/warden.mcfunction", '''
# Boss 热路径：空场只剩五个带类型/标签的存在性守卫。
execute as @e[tag=boss] unless score @s rpg_boom_id matches 1.. run function rpg:entities/warden/pseudo_id
execute if entity @e[tag=devil,limit=1] run function rpg:entities/warden/phase1
execute if entity @e[type=minecraft:vindicator,tag=devil2,limit=1] run function rpg:entities/warden/phase2
execute if entity @e[type=minecraft:armor_stand,tag=rpg.boss.slash,limit=1] run function rpg:entities/warden/slashes
execute if entity @e[type=minecraft:marker,tag=rpg.bossbar.probe,limit=1] run function rpg:entities/warden/bossbar_probe_tick
execute if entity @e[tag=boss,limit=1] run function rpg:entities/warden/bossbar_clock
''')


def optimize_legacy_projectiles():
    text = read("item/legacy/projectiles.mcfunction")
    marker = "execute as @e[type=#minecraft:arrows,tag=rpg.legacy.bubble] at @s run particle"
    assert marker in text, "legacy projectile active section changed"
    before, active = text.split(marker, 1)
    active = marker + active
    seen = "tag @e[type=#minecraft:arrows,tag=!rpg.legacy.seen] add rpg.legacy.seen"
    assert seen in before
    before = before.replace(seen, '''tag @e[type=#minecraft:arrows,tag=rpg.legacy.bubble] add rpg.legacy.active
tag @e[type=#minecraft:arrows,tag=rpg.legacy.burn] add rpg.legacy.active
tag @e[type=#minecraft:arrows,tag=rpg.legacy.hunter] add rpg.legacy.active
tag @e[type=#minecraft:arrows,tag=!rpg.legacy.seen] add rpg.legacy.seen''')
    write("item/legacy/projectiles_new.mcfunction", before)
    active_body = []
    for line in active.splitlines():
        m = re.match(r"execute as @e\[type=#minecraft:arrows,tag=rpg\.legacy\.(bubble|burn|hunter)\] at @s (.*)", line)
        if m:
            kind, tail = m.groups()
            if tail.startswith("run "):
                tail = tail[4:]
                active_body.append("execute if entity @s[tag=rpg.legacy.%s] run %s" % (kind, tail))
            else:
                active_body.append("execute if entity @s[tag=rpg.legacy.%s] %s" % (kind, tail))
            continue
        m = re.match(r"kill @e\[type=#minecraft:arrows,tag=rpg\.legacy\.(bubble|burn|hunter),nbt=\{inGround:1b\}\]", line)
        if m:
            active_body.append("execute if entity @s[tag=rpg.legacy.%s,nbt={inGround:1b}] run kill @s" % m.group(1))
            continue
        if line and not line.startswith("#"):
            raise AssertionError("legacy active projectile line changed: " + line)
    # 三种入口都已经被 rpg.legacy.active 收窄；落地检查只需做一次。
    active_body = [x for x in active_body if "nbt={inGround:1b}" not in x]
    active_body += [
        "execute if entity @s[nbt={inGround:1b}] run return run kill @s",
        "scoreboard players add @s rpg_proj_t 1",
        "execute if score @s rpg_proj_t matches 200.. run kill @s",
    ]
    write("item/legacy/projectiles_active.mcfunction", "\n".join(active_body))
    write("item/legacy/projectiles.mcfunction", '''
# 普通箭首次分类后离开；只有三种技能箭进入持续热路径。
execute if entity @e[type=#minecraft:arrows,tag=!rpg.legacy.seen,limit=1] run function rpg:item/legacy/projectiles_new
execute as @e[type=#minecraft:arrows,tag=rpg.legacy.active] at @s run function rpg:item/legacy/projectiles_active
''')
    add_objective("rpg_proj_t")


def optimize_old_hit_feedback():
    rel = "item/sword/off/off.mcfunction"
    prefix = "execute as @e at @s on attacker "
    text = read(rel)
    assert text.count(prefix) == 13
    # 保持原来的 line-major 顺序与组末统一 reset，保证横扫同刻多目标
    # 共享一次掷点；只把遍历域从全世界收紧到本刻受伤索引。
    body = text.replace(prefix, "execute as @e[tag=rpg.hurt] at @s on attacker ")
    write("item/sword/off/off_active.mcfunction", body)
    write(rel, '''# 空闲时只做一次存在性检查；active 保留 line-major/AoE 掷点语义。
execute if entity @e[tag=rpg.hurt,limit=1] run function rpg:item/sword/off/off_active
''')


def optimize_extra_projectiles():
    """Bind each tagged skill arrow once instead of re-scanning it per effect."""
    specs = (("deep_seek", "rpg.deep"),
             ("mischief", "rpg.mis"),
             ("rift", "rpg.rift"))
    for name, tag in specs:
        rel = "item/extra/%s/g0.mcfunction" % name
        prefix = "execute as @e[tag=%s] at @s " % tag
        body = []
        for line in read(rel).splitlines():
            if not line or line.startswith("#"):
                continue
            assert line.startswith(prefix), "%s: %s" % (rel, line)
            local = line[len(prefix):]
            if local.startswith("run "):
                local = local[4:]
            elif not local.startswith("execute "):
                local = "execute " + local
            # A projectile killed by collision must not continue into later faces.
            local = local.replace(" run kill @s", " run return run kill @s")
            body.append(local)
        assert len(body) in (13, 14), "%s: unexpected body size" % rel
        write("item/extra/%s/entity.mcfunction" % name, "\n".join(body))
        write(rel, "execute as @e[type=minecraft:arrow,tag=%s] at @s run function rpg:item/extra/%s/entity" % (tag, name))


def optimize_level_sync():
    rel = "level/player.mcfunction"
    lines = read(rel).splitlines()
    split = next(i for i, line in enumerate(lines)
                 if "player_level_ = @s player_level" in line)
    up, sync = lines[:split], lines[split:]
    up_prefix = "execute as @a at @s if score @s level > @s player_level run "
    assert all((not x) or x.startswith(up_prefix) for x in up)
    up_body = [x[len(up_prefix):] for x in up if x]
    sync_body = []
    prefix = "execute as @a at @s "
    for line in sync:
        assert line.startswith(prefix), line
        line = line[len(prefix):]
        if line.startswith("run "):
            line = line[4:]
        elif not line.startswith("execute "):
            line = "execute " + line
        sync_body.append(line)
    sync_body.append("scoreboard players operation @s rpg_hp_level = @s player_level")
    write("level/up.mcfunction", "\n".join(up_body))
    write("level/sync_health.mcfunction", "\n".join(sync_body))
    write("level/player_tick.mcfunction", '''
scoreboard players add @s player_level 0
execute if score @s level > @s player_level run function rpg:level/up
execute unless score @s rpg_hp_level = @s player_level run function rpg:level/sync_health
''')
    write(rel, "execute as @a at @s run function rpg:level/player_tick")
    add_objective("rpg_hp_level")


def player_value_local(line):
    plain = "execute as @a at @s "
    tagged = re.match(r"execute as @a\[tag=([^]]+)\] at @s run (.*)", line)
    if tagged:
        return "execute if entity @s[tag=%s] run %s" % tagged.groups()
    assert line.startswith(plain), line
    line = line[len(plain):]
    return line[4:] if line.startswith("run ") else "execute " + line


def optimize_player_values():
    rel = "command/com.mcfunction"
    text = read(rel)
    start = text.index("##武器数据读取")
    end = text.index("##武器等级输入输出")
    section = text[start:end]
    values = [player_value_local(x) for x in section.splitlines()[1:] if x]
    panel = "execute as @a[tag=rpg.h.player_tag1] at @s run item modify entity @s weapon.mainhand rpg:command/player_value"
    assert panel in text
    values.append("execute if entity @s[tag=rpg.h.player_tag1] run item modify entity @s weapon.mainhand rpg:command/player_value")
    replacement = '''##武器数据读取（5 刻一次；注册与锻造事件仍逐刻响应）
scoreboard players add @a rpg_com_clock 1
execute as @a[scores={rpg_com_clock=5..}] at @s run function rpg:command/com/player_values
scoreboard players set @a[scores={rpg_com_clock=5..}] rpg_com_clock 0

'''
    text = text[:start] + replacement + text[end:]
    text = text.replace(panel, "# 玩家面板数值并入 5 刻一次的 player_values。")
    old_feedback = '''execute as @e at @s on attacker if entity @s[scores={weapon_attack=0..},tag=rpg.h.weapon_tag1] run playsound minecraft:entity.warden.attack_impact player @s
execute as @e at @s on attacker if entity @s[scores={weapon_attack=0..},tag=rpg.h.weapon_tag1] run particle crit ~0.25 ~1.5 ~0.25 -0.5 -0.5 -0.5 1 10'''
    assert old_feedback in text
    text = text.replace(old_feedback,
        "execute as @e[tag=rpg.hurt] at @s on attacker if entity @s[scores={weapon_attack=0..},tag=rpg.h.weapon_tag1] run function rpg:command/com/weapon_feedback")
    write(rel, text)
    write("command/com/player_values.mcfunction", "\n".join(values))
    write("command/com/weapon_feedback.mcfunction", '''
playsound minecraft:entity.warden.attack_impact player @s
particle crit ~0.25 ~1.5 ~0.25 -0.5 -0.5 -0.5 1 10
''')
    add_objective("rpg_com_clock")


def cap_demon_bursts():
    changed = 0
    for n in range(8):
        for suffix, cap in (("", 72), ("_charge", 48)):
            rel = "taint/ult%d%s.mcfunction" % (n, suffix)
            lines = []
            for line in read(rel).splitlines():
                if "particle " in line:
                    parts = line.split()
                    if parts[-1] == "force":
                        parts[-1] = "normal"
                        try:
                            count = int(parts[-2])
                        except ValueError:
                            count = 0
                        if count > cap:
                            parts[-2] = str(cap)
                        line = " ".join(parts)
                        changed += 1
                lines.append(line)
            write(rel, "\n".join(lines))
    rel = "item/devil/star/star.mcfunction"
    text = read(rel).replace(" 3 500 force", " 3 80 normal")
    write(rel, text)
    return changed


def main():
    optimize_warden()
    optimize_legacy_projectiles()
    optimize_old_hit_feedback()
    optimize_extra_projectiles()
    optimize_level_sync()
    optimize_player_values()
    burst_lines = cap_demon_bursts()
    print("runtime hot paths: boss bodies collapsed, bars 10Hz, slash TTL 20t")
    print("runtime hot paths: level change-driven, player values 5t, hurt scans indexed")
    print("runtime hot paths: demon burst particle lines capped: %d" % burst_lines)


if __name__ == "__main__":
    main()
