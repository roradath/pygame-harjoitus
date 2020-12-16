# Peli on aika simppeli ja varmaan toteutuksen olisi voinut tehdä tyylikkäämminkin, mutta tällä mennään...
# Kyseessä on siis klassinen pingispeli, robottia liikutetaan ylös w-näppäimellä ja alas s-näppäimellä. 
# Hirviö liikkuu ylös ja alas nuolinäppäimillä. Peliä pelataan viisi erää ja useamman erän voittanut voittaa pelin.
# Ihan täysinhän tämä ei toteuta vaatimuksia pelin suhteen, koska mitään ei varsinaisesti kerätä, palloa vain heitetään...

import pygame

class PingPong:
    def __init__(self):
        pygame.init()

        self.robo = pygame.image.load("robo.png")
        self.hirvio = pygame.image.load("hirvio.png")
        self.pallo = pygame.image.load("kolikko.png")
        self.uusi_peli()

        self.korkeus = 350
        self.leveys = 600
        self.info = 50

        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus + self.info))

        self.fontti = pygame.font.SysFont("Arial", 20)

        pygame.display.set_caption("Pingis (Robotti liikkuu w ja s -näppäimillä, hirviö nuolinäppäimillä. Pelissä 5 erää.)")
        #robon koordinaatit
        self.x = 0
        self.y = 0
        #hirviön koordinaatit
        self.x2 = self.leveys-self.hirvio.get_width()
        self.y2 = 0
        #pallon koordinaatit
        self.x3 = self.leveys/2
        self.y3 = self.korkeus/2

        self.kello = pygame.time.Clock()

        self.ylos = False
        self.alas = False
        self.ylos2 = False
        self.alas2 = False

        self.silmukka()

    def uusi_peli(self):
        self.pisteet_hirvio = 0
        self.pisteet_robo = 0
        self.nopeus1 = 2
        self.nopeus2 = 2

    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            self.piirra_naytto()
            self.pallo_liikkeelle()

    def tutki_tapahtumat(self):
        #näppäinkomennot:
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_UP:
                    self.ylos2 = True
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas2 = True
                if tapahtuma.key == pygame.K_w:
                    self.ylos = True
                if tapahtuma.key == pygame.K_s:
                    self.alas = True
 
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_UP:
                    self.ylos2 = False
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas2 = False
                if tapahtuma.key == pygame.K_w:
                    self.ylos = False
                if tapahtuma.key == pygame.K_s:
                    self.alas = False

                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()

            if tapahtuma.type == pygame.QUIT:
                exit()
            
            if self.peli_lapi() == "robo" or self.peli_lapi == "hirvio":
                return

        #Robon ja hirviön liikkeet:
        if self.ylos and self.y > 0:
            self.y -= 2
        else:
            self.y += 0
        if self.alas and self.y+self.robo.get_height() < self.korkeus:
            self.y += 2
        else:
            self.y += 0

        if self.ylos2 and self.y2 > 0:
            self.y2 -= 2
        else:
            self.y2 += 0
        if self.alas2 and self.y2+self.hirvio.get_height() < self.korkeus:
            self.y2 += 2
        else:
            self.y2 += 0

    def pallo_liikkeelle(self):
        self.x3 += self.nopeus1
        self.y3 += self.nopeus2

        #pallon liikkeet:
        if self.nopeus1 > 0 and self.osuuko_hirvio():
            self.nopeus1 = self.nopeus1*-1
        if self.nopeus1 < 0 and self.osuuko_robotti():
            self.nopeus1 = self.nopeus1*-1
        if self.nopeus2 > 0 and self.y3+self.pallo.get_height() >= self.korkeus:
            self.nopeus2 = self.nopeus2*-1
        if self.nopeus2 < 0 and self.y3 <= 0:
            self.nopeus2 = self.nopeus2*-1
        
        #pallo missattu:      
        if self.nopeus1 > 0 and self.x3+self.pallo.get_width() >= self.leveys:
            self.nopeus1 = self.nopeus1*-1
            self.pisteet_robo += 1
        if self.nopeus1 < 0 and self.x3 <= 0:
            self.nopeus1 = self.nopeus1*-1
            self.pisteet_hirvio += 1
    
    def osuuko_hirvio(self):
        # näissä osumissa on vähän jotain häikkää, ei aina "osu" vaikka pitäisi. Välillä vauhti tuntuu vaikuttavan (eli kun hirviö tai robotti
        # pysähtyy palloa vastaan, pallo kimpoaa. Mutta välillä tämä onnistuu myös vauhdista.)
        if self.x3+self.pallo.get_width() == self.x2 and self.y3 > self.y2-self.pallo.get_height() and self.y3 < self.y2+self.pallo.get_height():
            return True
        return False
        
    def osuuko_robotti(self):
        if self.x+self.robo.get_width() == self.x3 and self.y3 > self.y-self.pallo.get_height() and self.y3 < self.y+self.pallo.get_height():
            return True
        return False
        
    def piirra_naytto(self):
        #Pelikentän ja pelaajien asettaminen:
        self.naytto.fill((108,255,0))
        self.naytto.blit(self.robo, (self.x, self.y))
        self.naytto.blit(self.hirvio, (self.x2, self.y2))
        self.naytto.blit(self.pallo, (self.x3, self.y3))
        pygame.draw.line(self.naytto, (255, 255, 255), (self.leveys/2, 0), (self.leveys/2, self.korkeus), 1)
        pygame.draw.line(self.naytto, (255, 255, 255), (0, self.korkeus), (self.leveys, self.korkeus), 1)

        #Tekstit:
        teksti = self.fontti.render("Robotin pisteet: " + str(self.pisteet_robo), True, (0, 0, 0))
        self.naytto.blit(teksti, (10, self.korkeus + 10))

        teksti = self.fontti.render("F2 = uusi peli", True, (0, 0, 0))
        self.naytto.blit(teksti, (190, self.korkeus + 10))

        teksti = self.fontti.render("Esc = sulje peli", True, (0, 0, 0))
        self.naytto.blit(teksti, (300, self.korkeus + 10))

        teksti = self.fontti.render("Hirviön pisteet: " + str(self.pisteet_hirvio), True, (0, 0, 0))
        self.naytto.blit(teksti, (450, self.korkeus + 10))

        if self.peli_lapi() == "hirvio":
            teksti = self.fontti.render("Hirviö voitti pelin!", True, (255, 0, 0))
            teksti_x = self.leveys / 2 - teksti.get_width() / 2
            teksti_y = self.korkeus / 2 - teksti.get_height() / 2
            pygame.draw.rect(self.naytto, (0, 0, 0,), (teksti_x, teksti_y, teksti.get_width(), teksti.get_height()))
            self.naytto.blit(teksti, (teksti_x, teksti_y))
            self.nopeus1 = 0
            self.nopeus2 = 0

        if self.peli_lapi() == "robo":
            teksti = self.fontti.render("Robotti voitti pelin!", True, (255, 0, 0))
            teksti_x = self.leveys / 2 - teksti.get_width() / 2
            teksti_y = self.korkeus / 2 - teksti.get_height() / 2
            pygame.draw.rect(self.naytto, (0, 0, 0,), (teksti_x, teksti_y, teksti.get_width(), teksti.get_height()))
            self.naytto.blit(teksti, (teksti_x, teksti_y))
            self.nopeus1 = 0
            self.nopeus2 = 0
    
        pygame.display.flip()
        self.kello.tick(60)

    def peli_lapi(self):
        #Kun 5 erää on pelattu, tarkistetaan kummalla on enemmän erävoittoja:
        while self.pisteet_hirvio+self.pisteet_robo == 5:
            if self.pisteet_hirvio >= 3:
                return "hirvio"
            if self.pisteet_robo >= 3:
                return "robo"

if __name__ == "__main__":
    PingPong()