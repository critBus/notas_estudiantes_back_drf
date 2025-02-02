from django.db import models






class Students(models.Model):
    ci = models.CharField(max_length=20, primary_key=True)
    address = models.CharField(max_length=255)
    grade = models.IntegerField(choices=[7, 8, 9])
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    reg_number = models.CharField(max_length=255)
    sex = models.CharField(max_length=10)
    graduate =models.BooleanField(default=False)
    baja = models.BooleanField()


class AltasBajas(models.Model):
    baja = models.BooleanField()
    date = models.DateField()
    municipality = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    school = models.CharField(max_length=255)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)


class Careers(models.Model):
    amount = models.IntegerField()
    name = models.CharField(max_length=255)

    

class Graduado(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    no_dematricula = models.CharField(max_length=255, blank=True, null=True)
    fecha_graduacion = models.DateField(blank=True, null=True)
    carrera = models.CharField(max_length=255, blank=True, null=True)
    nota_escalafon = models.FloatField(blank=True, null=True)
    no_escalafon = models.IntegerField(blank=True, null=True)

    

class NotaGraduado(models.Model):
    nombreasignatura = models.CharField(max_length=255)
    as_nota = models.FloatField(blank=True, null=True)
    tcp1 = models.FloatField(blank=True, null=True)
    tcp2 = models.FloatField(blank=True, null=True)
    prueba_final = models.FloatField(blank=True, null=True)
    nota_final = models.FloatField(blank=True, null=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)

    class Meta:
        db_table = 'notagraduado'

class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    grade = models.IntegerField()
    name = models.CharField(max_length=255)
    tcp2 = models.BooleanField()

class Notes(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    acs = models.FloatField(blank=True, null=True)
    final_note = models.FloatField(blank=True, null=True)
    final_exam = models.FloatField(blank=True, null=True)
    tcp1 = models.FloatField(blank=True, null=True)
    tcp2 = models.FloatField(blank=True, null=True)


class Otorgamiento(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    year_graduacion = models.IntegerField(blank=True, null=True)
    carrera = models.CharField(max_length=255, blank=True, null=True)
    nota_escalafon = models.FloatField(blank=True, null=True)
    no_escalafon = models.IntegerField(blank=True, null=True)

    

class StudentCareer(models.Model):
    career = models.ForeignKey(Careers, on_delete=models.CASCADE)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    index = models.IntegerField()






    

