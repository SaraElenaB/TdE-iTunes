from database.DB_connect import DBConnect
from model.album import Album


class DAO():

    # --------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllAlbum(dMin):

        cnx= DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        ris= []

        query=""" select a.* , sum(t.Milliseconds)/1000/60 as dTotMin
                  from track t , album a 
                  where t.AlbumId = a.AlbumId
                  group by AlbumId 
                  having dTotMin >= %s"""
                  #puoi farlo perchè fai la group by su una chiave primaria

        cursor.execute(query, (dMin,))
        for row in cursor:
            ris.append( Album(**row))

        cursor.close()
        cnx.close()
        return ris

    # --------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getAllEdges(idMapAlbum):

        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        ris = []

        #distinc --> rende tutto lento!!
        query = """ select distinct t1.AlbumId as a1, t2.AlbumId as a2
                    from playlisttrack p1, playlisttrack p2, track t1, track t2
                    where t1.TrackId = p1.TrackId
                    and  t2.TrackId = p2.TrackId
                    and p1.PlaylistId = p2.PlaylistId
                    and t1.AlbumId < t2.AlbumId"""
                    # <,> --> toglie i doppioni
                    # distinct --> archi molteplici, stessa coppia in diverse playlist
                    # ricordati di mettere solo nodi --> quindi la durata

        cursor.execute(query,)
        for row in cursor:
            # altrimenti errore perchè nella query ho tutti i possibili archi
            if row["a1"] in idMapAlbum and row["a2"] in idMapAlbum:
                ris.append( (idMapAlbum[row["a1"]],
                            idMapAlbum[row["a2"]]) )

        cursor.close()
        cnx.close()
        return ris




