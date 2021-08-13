import sqlite3

conn = sqlite3.connect('guild.db')
c = conn.cursor()


# c.execute("""CREATE TABLE event_votes (
#             user_id INTEGER DEFAULT 0,
#             season_number INTEGER DEFAULT 0,
#             total_votes INTEGER DEFAULT 0,
#             UNIQUE(user_id)
#             )""")

c.execute("""INSERT INTO config VALUES(
            'season_number',
            2
            )""")

# FOR INSERTS
# c.execute("""UPDATE badges_master
#             SET position = position+1
#             WHERE id >= 8""")
#
# c.execute("""INSERT INTO badges_master VALUES(
#             '8',
#             'Season finalist!',
#             'Be a season finalist.',
#             'https://media.discordapp.net/attachments/822229241511936090/864592892147138600/Season_Finalist.png?width=654&height=676',
#             '8'
#             )""")

# FOR REMOVALS
# c.execute("""UPDATE badges_master
#             SET position = position+1
#             WHERE id >= 8""")
#
# c.execute("""INSERT INTO badges_master VALUES(
#             '8',
#             'Season finalist!',
#             'Be a season finalist.',
#             'https://media.discordapp.net/attachments/822229241511936090/864592892147138600/Season_Finalist.png?width=654&height=676',
#             '8'
#             )""")

# rows = c.execute("""SELECT *
#                     FROM badges_master
#                     ORDER BY position ASC""").fetchall()

# c.execute("""INSERT INTO Destination SELECT * FROM Source""")
# print(rows)

# c.execute("""ALTER TABLE badges_users_stats ADD wants_notifications INTEGER""")

conn.commit()

conn.close()
