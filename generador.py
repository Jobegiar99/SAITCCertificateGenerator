#Copyright SAITC 2020-2021
#MIT LICENSE

from PIL import Image, ImageDraw, ImageFont
import pandas as pd 
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

userEmail = input("Ingresa el correo desde el cual vas a enviar los certificados")
userPassw = input("Ingresa la contraseña de tu correo")
userCSV   = input("Ingresa el nombre del archivo csv (debe de estar en el mismo directorio que este archivo)")
csv = pd.read_csv(userCSV)

def generateCertificates():

    for index in range(len(csv)):
        nombre = csv.iloc[index]['Nombre']
        apellidoPaterno = csv.iloc[index]['Apellido paterno']
        apellidoMaterno = csv.iloc[index]['Apellido materno']
        correo = csv.iloc[index]['Dirección de correo electrónico']
        tituloCertificado = "Por su participación en el Game Jam \nSALAD, SAIMI y SAITC agradecen a "
                                           

        nombreCompleto = nombre + " " + apellidoPaterno + " " + apellidoMaterno

        fecha = "Dado el 18 de abril del 2021"

        image = Image.open('Diploma.jpg')

        firmaSAITC = Image.open(r'./firmaSAITC.png')
        fondoSAITC = Image.new('RGB', (firmaSAITC.width, int(firmaSAITC.height / 5)), color = 'rgba(255,255,255,50)')

        firmaSALAD = Image.open(r'./firmaSALAD.png')
        fondoSALAD = Image.new('RGB', (firmaSAITC.width, int(firmaSAITC.height / 5)), color = 'rgba(255,255,255,50)')

        firmaSAIMI = Image.open(r'./firmaSaimi.png')
        fondoSAIMI = Image.new('RGB', (firmaSAITC.width, int(firmaSAITC.height / 5)), color = 'rgba(255,255,255,50)')


        firmaSAIMI = firmaSAIMI.resize((600 ,300))
        firmaSALAD = firmaSALAD.resize((600,300))
        
        draw = ImageDraw.Draw(image)

        fontTitle = ImageFont.truetype(r'\\Pokemon Classic.ttf', size= 80 )
        fontName = ImageFont.truetype(r'\\Pokemon Classic.ttf', size= 100 )
        fontFecha = ImageFont.truetype(r'\\Pokemon Classic.ttf', size= 60 )
        fontSA = ImageFont.truetype(r'\\Pokemon Classic.ttf', size= 30 )

        SAITC = "                 Bernardo Girón\nPresidente SAITC 2020-2021"
        SALAD = "                  César Tijerina  \nPresidente SALAD 2020-2021"
        SAIMI = "                Luna Méndoza \nPresidenta SAIMI 2020-2021"

        color = 'rgb(255, 255, 255)' #blanco

        W = image.width
        H = image.height
        w, h = draw.textsize(nombreCompleto, font = fontName)
        (xNombre, yNombre) = ((W-w)/2, (H-h)/2)
        (xTitulo, yTitulo) = ((image.width / 2) - (image.width / 2.97) + 100 , image.height/2 - (image.height / 5))
        (xFecha, yFecha) = ((image.width / 2) - (image.width / 5.5) - 50 , image.height/2 + (image.height / 2.5))
        (xSAITC, ySA) = ((image.width / 2) - (image.width / 5.5) + 220 , image.height/2 + (image.height / 3))
        (xSALAD, ySA) = ((image.width / 2) - (image.width / 5.5) + 1420 , image.height/2 + (image.height / 3))
        (xSAIMI, ySA) = ((image.width / 2) - (image.width / 5.5) - 920 , image.height/2 + (image.height / 3))

        # draw the message on the background
        
        draw.text( (xTitulo, yTitulo), tituloCertificado, fill=color, font = fontTitle, stroke_fill = '#211A3F', stroke_width = 15)

        draw.text( (xNombre, yNombre), nombreCompleto, fill=color, font = fontName, stroke_fill = '#211A3F', stroke_width = 15 )

        draw.text( (xFecha, yFecha) , fecha, fill = color, font = fontFecha, stroke_fill = '#211A3F', stroke_width = 15 )

        draw.text( (xSAITC, ySA) , SAITC , fill = color, font = fontSA, stroke_fill = '#211A3F', stroke_width = 15 )

        draw.text( (xSAIMI, ySA) , SAIMI , fill = color, font = fontSA, stroke_fill = '#211A3F', stroke_width = 15 )

        draw.text( (xSALAD, ySA) , SALAD , fill = color, font = fontSA, stroke_fill = '#211A3F', stroke_width = 15 )

        image.paste(firmaSAITC, (int(xSAITC) + 150, int(ySA) - 400 ), mask=firmaSAITC) 

        image.paste(firmaSALAD, (int(xSALAD) + 120, int(ySA) - 400 ), mask=firmaSALAD) 

        image.paste(firmaSAIMI, (int(xSAIMI) + 90, int(ySA) - 400 ), mask=firmaSAIMI) 

        # save the edited image
        
        image.save(nombreCompleto + ".png")
        sendMail(nombreCompleto,correo)
    

def sendMail( name, email ):
    port = 465  # For SSL

    # Create a secure SSL context

    attachment = "./"+ name+ ".png"
    message = MIMEMultipart()
    message["Subject"] = "Certificado por participar en el Game Jam Internacional"
    message["From"] = userEmail
    message["To"] = email

    msgText = MIMEText('<b>%s</b><br><img src="cid:%s"><br>' % ("", attachment), 'html')
    fp = open(attachment, 'rb')                                                    
    img = MIMEImage(fp.read())
    fp.close()
    img.add_header('Content-ID', '<{}>'.format(attachment))
    message.attach(img)


    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    html = """\
    <html>
    <body align = "center">
        <img width = 50% height = 50% src = "https://lh3.googleusercontent.com/yRGddEhLR8e-ioFew5OAO8PECQfQi2dfPbblKbrBuxWh1mJfyOzPSE0xmSNGjk_6_6poi-EW65IxWszs-LkZ42XeAarL-SjR4um_zZghoRyNerPvQSt-zORrgE-ExwhvBogHW2E-dN-p32Jqrh-P1OlcEjm_npTTU-OV395RX39eau25xkPhpxki45Gwv2W_6cerpk5ESZnAGvxiWRwcPDICoj3DrHb-TKMTQzcFnPaQvuOyEfeZeP8LG7qmAcLidIALoxN8m3nrEW96Llc91NnoL50WUm6YfKqffXK_4iAvOtCQOg3YVk_UYF9C1UOixJxN6yGkfJtRC25WtUbTJUukuAuayAPXMW58OUvWyg38Tit9gRe5lQ2OtX9lyE6IVGMSVwIOsxspbvqhG-txJ8uZvqcvXmjETDGJKGbDrBq_0B3twVolNs0NE1nvV03Py2IxIsBuGGT3EbAJKaw5mWHH0_BX3tbMf3ridfu7k3kJSpANsNHMuswT7esbZrPt0RzGkItjrRxEjpMX2l8zRsIXU0QW8YY7QzAbcDu3olpQpyIFfud-Vl3y_zCf5TifwleDFVlr3HotM7rr0goRaVGC_m0gxss5ANTAiqr6zO41kW7HIYqLOHi0lrGj4EN2utD-jln3JPO0Lx4s1_CqX8cwN_c6k53QFgAcJf5HhUcuTocrpCl_2thLUBe_XsoqF7PAKC53LG2lb-aE0iUoNxHS=w1600-h400-no?authuser=0">
            <br>
            <br>
        <p>Hola """ + name + """,
            <br><br>
            Este es un mensaje automatizado con el cual te enviamos tu certificado. <br>
            Si llega a haber algun problema con la colocacion del nombre por favor envia un mensaje a la cuenta de<br>
            instagram de la saitc <a href = "https://www.instagram.com/saitc.mty/"> @saitc.mty </a><br>
            <br><br>
            Podrás acceder a las grabaciones por medio de <a href = "driveURL"> este enlace </a>, todavía se están procesando y subiendo.
            <br><br>
            Espero que hayas disfrutado de los talleres :) Sigue la cuenta oficial de la saitc para enterarte de más eventos
            
        </p>
    </body>
    </html>
    """

    htmlToAdd = MIMEText(html, "html")
    message.attach(htmlToAdd)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(userEmail, userPassw)

        server.sendmail(
            userEmail, email, message.as_string()
        )




